<script>
import axios from 'axios'

export default {
  name: 'BankSearch',
  data() {
    return {
      searchKeyword: '',
      banks: [],
      loading: false,
      error: null,
      map: null,
      markers: [],
      currentLocation: {
        latitude: null,
        longitude: null
      },
      lastSearchKeyword: '',
      showResearchButton: false,
      showSidebar: localStorage.getItem('showSidebar') !== 'false',
      currentInfowindow: null,  // 현재 열린 인포윈도우 추적
      activeMarker: null,       // 현재 활성화된 마커 추적
      infowindows: [] // 인포윈도우 배열 추가
    }
  },
  mounted() {
    const script = document.createElement('script')
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_API_KEY}&autoload=false`
    script.async = true
    script.addEventListener('load', () => {
      kakao.maps.load(() => {
        this.initializeMap()
        this.initializeMapEvents()
      })
    })
    document.head.appendChild(script)
  },
  beforeDestroy() {
    this.clearMarkers();
    if (this.map) {
      kakao.maps.event.removeListener(this.map, 'dragend');
      kakao.maps.event.removeListener(this.map, 'zoom_changed');
    }
  },
  methods: {
    initializeMap() {
      const container = document.getElementById('map')
      const options = {
        center: new kakao.maps.LatLng(37.5665, 126.9780),
        level: 3
      }
      this.map = new kakao.maps.Map(container, options)
    },
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
      localStorage.setItem('showSidebar', this.showSidebar);
    },
    initializeMapEvents() {
      kakao.maps.event.addListener(this.map, 'dragend', this.showResearchButtonIfNeeded)
      kakao.maps.event.addListener(this.map, 'zoom_changed', this.showResearchButtonIfNeeded)
    },
    showResearchButtonIfNeeded() {
      if (this.lastSearchKeyword || (this.currentLocation.latitude && this.currentLocation.longitude)) {
        this.showResearchButton = true
      }
    },
    debounce(func, wait) {
      let timeout
      return (...args) => {
        clearTimeout(timeout)
        timeout = setTimeout(() => func.apply(this, args), wait)
      }
    },
    async getCurrentLocation() {
      this.loading = true;
      this.error = null;
      
      if (!navigator.geolocation) {
        this.error = '이 브라우저에서는 위치 정보를 지원하지 않습니다.';
        this.loading = false;
        return;
      }

      try {
        const position = await new Promise((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject, {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
          });
        });

        this.currentLocation = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        };

        const currentPosition = new kakao.maps.LatLng(
          position.coords.latitude,
          position.coords.longitude
        );
        
        this.map.setCenter(currentPosition);
        this.map.setLevel(3);

        // 키워드가 있는 경우 keyword 검색 API를, 없는 경우 nearby API를 호출
        if (this.searchKeyword.trim()) {
          await this.searchByKeywordAndLocation();
        } else {
          await this.searchNearby();
        }

      } catch (error) {
        this.error = '위치 정보를 가져올 수 없습니다: ' + error.message;
        console.error('Geolocation error:', error);
      } finally {
        this.loading = false;
      }
    },

    // 새로 추가하는 메소드
    async searchByKeywordAndLocation() {
      this.loading = true;
      this.error = null;

      try {
        const bounds = this.map.getBounds();
        const sw = bounds.getSouthWest();
        const ne = bounds.getNorthEast();

        const response = await axios.get('/api/v1/locations/banks/search/', {
          params: {
            keyword: this.searchKeyword,
            sw_lat: sw.getLat(),
            sw_lng: sw.getLng(),
            ne_lat: ne.getLat(),
            ne_lng: ne.getLng()
          }
        });

        if (response.data.documents && response.data.documents.length > 0) {
          this.banks = response.data.documents;
          this.updateMap();
          this.showResearchButton = false;
          this.lastSearchKeyword = this.searchKeyword;
        } else {
          this.error = '현재 위치 주변에 검색 결과가 없습니다.';
          this.banks = [];
        }
      } catch (error) {
        console.error('Error:', error);
        this.error = '검색 중 오류가 발생했습니다.';
        this.banks = [];
      } finally {
        this.loading = false;
      }
    },
    async searchNearbyWithKeyword() {
      this.loading = true;
      this.error = null;

    try {
        const response = await axios.get('/api/v1/locations/banks/search/', {
          params: {
            keyword: this.searchKeyword,
            latitude: this.currentLocation.latitude,
            longitude: this.currentLocation.longitude,
            radius: 1000
          }
        });

        if (response.data?.documents?.length > 0) {
          this.banks = response.data.documents;
          this.updateMap();
          this.showResearchButton = false;
        } else {
          this.error = '주변에 검색 결과가 없습니다.';
          this.banks = [];
        }
      } catch (error) {
        console.error('Error:', error);
        this.error = error.response?.data?.message || '검색 중 오류가 발생했습니다.';
        this.banks = [];
      } finally {
        this.loading = false;
      }
    },

    async searchNearby() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get('/api/v1/locations/banks/nearby/', {
          params: {
            latitude: this.currentLocation.latitude,
            longitude: this.currentLocation.longitude,
            radius: 1000
          }
        });

        if (response.data?.banks?.length > 0) {
          this.banks = response.data.banks;
          this.updateMap();
          this.showResearchButton = false;
        } else {
          this.error = '주변에 은행이 없습니다.';
          this.banks = [];
        }
      } catch (error) {
        console.error('Error:', error);
        this.error = error.response?.data?.message || '은행 검색 중 오류가 발생했습니다.';
        this.banks = [];
      } finally {
        this.loading = false;
      }
    },
    async searchByKeyword() {
      if (!this.searchKeyword.trim()) {
        this.error = '검색어를 입력해주세요.';
        return;
      }

      this.loading = true;
      this.error = null;
      this.lastSearchKeyword = this.searchKeyword;
      
      try {
        const response = await axios.get('/api/v1/locations/banks/search/', {
          params: {
            keyword: this.searchKeyword
          }
        });

        if (response.data?.documents?.length > 0) {
          this.banks = response.data.documents;
          this.updateMap();
          this.showResearchButton = false;
        } else {
          this.error = '검색 결과가 없습니다.';
          this.banks = [];
        }
      } catch (error) {
        console.error('Search Error:', error);
        this.error = error.response?.data?.message || 
                    error.message || 
                    '검색 중 오류가 발생했습니다.';
        this.banks = [];
      } finally {
        this.loading = false;
      }
    },
    async handleResearch() {
      if (this.loading) return;
      
      const bounds = this.map.getBounds();
      const sw = bounds.getSouthWest();
      const ne = bounds.getNorthEast();
      
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get('/api/v1/locations/banks/search/', {
          params: {
            keyword: this.lastSearchKeyword || '*',  // Use wildcard or default value
            sw_lat: sw.getLat(),
            sw_lng: sw.getLng(),
            ne_lat: ne.getLat(),
            ne_lng: ne.getLng()
          }
        });

        if (response.data?.documents?.length > 0) {
          this.banks = response.data.documents;
          this.updateMarkersOnly();
          this.showResearchButton = false;
        } else {
          this.error = '이 지역에 검색 결과가 없습니다.';
          this.banks = [];
        }
      } catch (error) {
        console.error('Error:', error);
        this.error = error.response?.data?.message || '검색 중 오류가 발생했습니다.';
        this.banks = [];
      } finally {
        this.loading = false;
      }
    },
    // async handleResearch() {
    //   if (this.loading) return
      
    //   const bounds = this.map.getBounds()
    //   const sw = bounds.getSouthWest()
    //   const ne = bounds.getNorthEast()
      
    //   this.loading = true
    //   this.error = null
    // try {
    //     // 키워드가 있으면 키워드 검색, 없으면 주변 검색
    //     if (this.lastSearchKeyword) {
    //       const response = await axios.get('/api/v1/locations/banks/search/', {
    //         params: {
    //           keyword: this.lastSearchKeyword,
    //           sw_lat: sw.getLat(),
    //           sw_lng: sw.getLng(),
    //           ne_lat: ne.getLat(),
    //           ne_lng: ne.getLng()
    //         }
    //       })
    //       if (response.data.documents) {
    //         this.banks = response.data.documents
    //         this.updateMarkersOnly()
    //         this.showResearchButton = false
    //       } else {
    //         this.error = '검색 결과가 없습니다.'
    //       }
    //     } else {
    //       // 주변 검색 API 호출
    //       const response = await axios.get('/api/v1/locations/banks/nearby/', {
    //         params: {
    //           latitude: this.map.getCenter().getLat(),
    //           longitude: this.map.getCenter().getLng(),
    //           radius: 1000
    //         }
    //       })
    //       if (response.data.banks) {
    //         this.banks = response.data.banks
    //         this.updateMarkersOnly()
    //         this.showResearchButton = false
    //       } else {
    //         this.error = '주변에 은행이 없습니다.'
    //       }
    //     }
    //   } catch (error) {
    //     console.error('Error:', error)
    //     this.error = '검색 중 오류가 발생했습니다.'
    //   } finally {
    //     this.loading = false
    //   }
    // },
    updateMap() {
      if (!this.map || !this.banks.length) return
      this.clearMarkers()
      const bounds = new kakao.maps.LatLngBounds()
      this.banks.forEach(bank => {
        const position = new kakao.maps.LatLng(bank.y, bank.x)
        const marker = this.createMarker(position, bank)
        bounds.extend(position)
      })
      this.map.setBounds(bounds)
    },
    updateMarkersOnly() {
      if (!this.map || !this.banks.length) return
      this.clearMarkers()
      this.banks.forEach(bank => {
        const position = new kakao.maps.LatLng(bank.y, bank.x)
        this.createMarker(position, bank)
      })
    },
    clearMarkers() {
      // 마커와 인포윈도우 모두 제거
      this.markers.forEach(marker => marker.setMap(null));
      this.infowindows.forEach(info => info.close());
      this.markers = [];
      this.infowindows = [];
    },
    createMarker(position, bank) {
      // 마커 생성
      const marker = new kakao.maps.Marker({ position });
      marker.setMap(this.map);
      this.markers.push(marker);

      // 인포윈도우 생성
      const infowindow = new kakao.maps.InfoWindow({
        content: this.createInfoWindowContent(bank),
        removable: true
      });
      this.infowindows.push(infowindow);

      // 인포윈도우 닫기 이벤트 리스너
      kakao.maps.event.addListener(infowindow, 'closeclick', () => {
        this.currentInfowindow = null;
        this.activeMarker = null;
      });

      // 마커 클릭 이벤트 리스너
      kakao.maps.event.addListener(marker, 'click', () => {
        // 현재 열린 인포윈도우가 있으면 닫기
        if (this.currentInfowindow) {
          this.currentInfowindow.close();
          
          // 같은 마커를 다시 클릭한 경우
          if (this.activeMarker === marker) {
            this.currentInfowindow = null;
            this.activeMarker = null;
            return;
          }
        }

        // 새로운 인포윈도우 열기
        infowindow.open(this.map, marker);
        this.currentInfowindow = infowindow;
        this.activeMarker = marker;

        // 해당 은행 카드로 스크롤
        const bankCard = document.querySelector(`[data-bank-id="${bank.id}"]`);
        if (bankCard) {
          bankCard.scrollIntoView({ behavior: 'smooth' });
        }
      });

      return marker;
    },
    moveToBank(bank) {
      const position = new kakao.maps.LatLng(bank.y, bank.x);
      this.map.setCenter(position);
      this.map.setLevel(3);
      
      // 현재 열린 인포윈도우 닫기
      if (this.currentInfowindow) {
        this.currentInfowindow.close();
      }
      
      // 해당 마커 찾기
      const marker = this.markers.find(m => 
        m.getPosition().equals(position)
      );
      
      if (marker) {
        // 새로운 인포윈도우 생성 및 표시
        const infowindow = new kakao.maps.InfoWindow({
          content: this.createInfoWindowContent(bank),
          removable: true
        });
        
        infowindow.open(this.map, marker);
        this.currentInfowindow = infowindow;
        this.activeMarker = marker;
      }
    },
    createInfoWindowContent(bank) {
      return `
        <div style="padding:10px;width:250px;font-size:12px;">
          <h4 style="margin:0 0 5px;font-size:14px;color:#333;">${bank.place_name}</h4>
          ${bank.phone ? `<p style="margin:5px 0;color:#666;"><span style="color:#2196F3;">☎</span> ${bank.phone}</p>` : ''}
          <p style="margin:5px 0;color:#666;"><span style="color:#4CAF50;">📍</span> ${bank.address_name}</p>
          ${bank.road_address_name ? `<p style="margin:5px 0;color:#888;font-size:11px;">(도로명: ${bank.road_address_name})</p>` : ''}
          ${bank.distance ? `<p style="margin:5px 0;color:#666;"><span style="color:#FF9800;">🚶</span> ${(bank.distance / 1000).toFixed(1)}km</p>` : ''}
        </div>
      `;
    }
  }
}
</script>


<template>
  <div class="bank-search">
    <h1 class="title">은행찾기</h1>
    
    <div class="content-wrapper">
      <!-- 왼쪽 사이드바 -->
      <div class="left-sidebar">
        <!-- 검색 섹션 -->
        <div class="search-section">
          <div class="search-form">
            <div class="search-box">
              <input 
                type="text" 
                v-model="searchKeyword" 
                placeholder="은행명을 입력하세요"
                @keyup.enter="searchByKeyword"
              >
              <button @click="searchByKeyword" class="search-btn">
                <i class="fas fa-search"></i> 검색
              </button>
            </div>
            <button @click="getCurrentLocation" class="location-btn">
              <i class="fas fa-location-arrow"></i> 내 위치에서 찾기
            </button>
          </div>
        </div>

        <!-- 검색 결과 목록 -->
        <div class="results-section">
          <div v-if="loading" class="status-message loading">
            <i class="fas fa-spinner fa-spin"></i> 검색 중...
          </div>
          <div v-else-if="error" class="status-message error">
            <i class="fas fa-exclamation-circle"></i> {{ error }}
          </div>
          <div v-else-if="banks.length > 0" class="bank-list">
            <div class="results-count">
              검색결과 {{ banks.length }}개
            </div>
            <div v-for="bank in banks" 
                 :key="bank.id" 
                 class="bank-card"
                 :data-bank-id="bank.id"
                 @click="moveToBank(bank)"
                 style="cursor: pointer"
                 >
              <div class="bank-header">
                <i class="fas fa-university"></i>
                <h3>{{ bank.place_name }}</h3>
                <span v-if="bank.distance" class="distance-badge">
                  {{ (bank.distance / 1000).toFixed(1) }}km
                </span>
              </div>
              <div class="bank-info">
                <p class="address">
                  <i class="fas fa-map-marker-alt"></i>
                  {{ bank.address_name }}
                  <span v-if="bank.road_address_name" class="road-address">
                    (도로명: {{ bank.road_address_name }})
                  </span>
                </p>
                <p v-if="bank.phone" class="phone">
                  <i class="fas fa-phone"></i>
                  {{ bank.phone }}
                </p>
              </div>
              <a :href="bank.place_url" target="_blank" class="detail-btn">
                상세정보 보기 <i class="fas fa-arrow-right"></i>
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- 오른쪽 지도 섹션 -->
      <div class="map-section">
        <div id="map" class="map-container">
          <div v-if="showResearchButton" class="research-button-container">
            <button @click="handleResearch" class="research-btn">
              <i class="fas fa-sync-alt"></i> 이 지역에서 다시 찾기
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.bank-search {
  font-family: 'GowunDodum-Regular', sans-serif;
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem;
  background-color: #FFFEFB;
  height: 90vh;
  display: flex;
  flex-direction: column;
}


.title {
  font-family: 'JalnanFont', sans-serif;
  text-align: center;
  color: #73553C;
  font-size: 2rem;
  margin: 1.5rem 0;
}

.search-section {
  background-color: #FEF0AC;
  padding: 1.5rem;
  border-radius: 15px;
  margin-bottom: 2rem;
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.search-box {
  display: flex;
  gap: 0.5rem;
}

.location-btn {
  width: 100%;
}

input {
  flex: 1;
  padding: 0.8rem 1rem;
  border: 2px solid #FDE49B;
  border-radius: 8px;
  font-size: 1rem;
  font-family: 'jjinbbangM', sans-serif;
}

.search-btn, .location-btn {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-family: 'jjinbbangB', sans-serif;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-btn {
  background-color: #73553C;
  color: #FFFEFB;
}

.location-btn {
  background-color: #3D0F0E;
  color: #FFFEFB;
}

.content-wrapper {
  flex: 1;
  display: flex;
  gap: 1.5rem;
  min-height: 0; /* 중요: flex 컨테이너 내부 스크롤을 위해 필요 */
  padding: 1rem;
  margin-top: 1rem; /* 제목과의 간격 추가 */
}

.left-sidebar {
  width: 350px;
  display: flex;
  flex-direction: column;
  background: #FFFEFB;
  border-radius: 15px;
  border: 3px solid #FDE49B;
  overflow: hidden;
  flex-shrink: 0; /* 사이드바 크기 고정 */
}

.search-section {
  padding: 1rem;
  background-color: #FEF0AC;
  border-radius: 12px 12px 0 0;
  flex-shrink: 0; /* 검색 영역 크기 고정 */
  margin: 0;
}

.results-section {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  min-height: 0; /* 스크롤을 위해 필요 */
}

.map-section {
  flex: 1;
  position: relative;
  min-width: 0; /* flex item 내부 오버플로우 방지 */
  border-radius: 15px;
  overflow: hidden;
  border: 3px solid #FDE49B;
}

.map-container {
  width: 100%;
  height: 100%;
  border-radius: 12px;
  border: none;
}

.research-button-container {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
}

.research-btn {
  background-color: #FFFEFB;
  padding: 0.8rem 1.2rem;
  border-radius: 20px;
  box-shadow: 0 2px 4px rgba(115, 85, 60, 0.2);
  font-size: 0.9rem;
  border: 2px solid #FDE49B;
  color: #73553C;
  font-family: 'jjinbbangM', sans-serif;
}

.results-sidebar {
  position: absolute;
  top: 0;
  right: 0;
  width: 380px;
  height: 100%;
  background: #FFFEFB;
  border-left: 3px solid #FDE49B;
  transition: transform 0.3s ease;
  overflow-y: auto;
  border-radius: 15px;
  z-index: 10;
  box-shadow: -2px 0 10px rgba(115, 85, 60, 0.1);
}

.sidebar-hidden {
  transform: translateX(100%);
}

.toggle-sidebar-btn {
  position: absolute;
  left: -40px;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 60px;
  background: #FDE49B;
  border: none;
  border-radius: 8px 0 0 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #73553C;
  font-size: 1.2rem;
  transition: all 0.3s ease;
  z-index: 11;
}
.toggle-sidebar-btn:hover {
  background: #73553C;
  color: #FFFEFB;
}

.results-count {
  padding: 1rem;
  margin: 0;
  font-family: 'jjinbbangB', sans-serif;
}

.bank-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.bank-card {
  margin-bottom: 0.8rem;
  background: #FFFEFB;
  border: 1px solid #FDE49B;
  border-radius: 8px;
  padding: 0.8rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: all 0.2s ease;
}

.bank-header {
  display: flex;
  font-size: 0.9rem;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem 0;
  margin-bottom: 0.3rem;
  color: #73553C;
  border-bottom: 1px solid #FDE49B;
}


.bank-info {
  padding: 0.2rem 0;
  color: #3D0F0E;
  font-size: 0.75rem;
  line-height: 1.3;
}

.distance-badge {
  background: #FEF0AC;
  color: #73553C;
  padding: 0.25rem 0.5rem;
  border-radius: 16px;
  font-size: 0.85rem;
  margin-left: auto;
}

.detail-btn {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  margin-top: 0.5rem;
  background: #FEF0AC;
  color: #73553C;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.7rem;
}

.detail-btn:hover {
  background: #73553C;
  color: #FFFEFB;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(115, 85, 60, 0.15);
}


/* 스크롤바 스타일링 */
.bank-list::-webkit-scrollbar {
  width: 8px;
}

.bank-list::-webkit-scrollbar-track {
  background: #FEF0AC;
  border-radius: 4px;
}

.bank-list::-webkit-scrollbar-thumb {
  background: #73553C;
  border-radius: 4px;
}

.bank-list::-webkit-scrollbar-thumb:hover {
  background: #3D0F0E;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #73553C;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.error {
  text-align: center;
  padding: 20px;
  color: #3D0F0E;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

@media (max-width: 1024px) {
  .bank-search {
    padding: 0.8rem;
  }

  .title {
    font-size: 2rem;
    margin: 0.8rem 0;
  }
}

@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
    gap: 1rem;
    height: calc(100vh - 150px);
  }

  .left-sidebar {
    width: 100%;
    height: 50%;
    min-height: 300px;
    max-height: 50vh;
  }

  .map-section {
    height: 50%;
    min-height: 300px;
  }

  .search-section {
    padding: 1rem;
  }

  .bank-card {
    margin-bottom: 0.8rem;
    padding: 1rem;
  }

  .bank-header {
    padding: 0.5rem;
    font-size: 0.9rem;
  }

  .bank-info {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .bank-search {
    padding: 0.5rem;
  }

  .title {
    font-size: 1.5rem;
    margin: 0.5rem 0;
  }

  .search-section {
    padding: 0.8rem;
  }

  .search-form {
    gap: 0.8rem;
  }

  .search-box {
    flex-direction: column;
    gap: 0.5rem;
  }

  .search-btn,
  .location-btn {
    width: 100%;
    padding: 0.8rem;
    font-size: 0.9rem;
  }

  input {
    width: 100%;
    padding: 0.8rem;
  }

  .bank-card {
    padding: 0.8rem;
    margin-bottom: 0.5rem;
  }

  .results-count {
    padding: 0.8rem;
    font-size: 0.9rem;
  }

  .detail-btn {
    padding: 0.6rem;
    font-size: 0.9rem;
  }
}

</style>