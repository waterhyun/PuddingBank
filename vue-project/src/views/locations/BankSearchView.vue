<template>
  <div class="bank-search">
    <h2 class="title">내 근처 은행 찾기</h2>
    
    <!-- 검색 폼 -->
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

    <!-- 지도와 검색 결과 영역 -->
    <div class="content-container">
      <!-- 지도 영역 -->
      <div class="map-section">
        <div id="map" class="map-container">
          <div v-if="showResearchButton" class="research-button-container">
            <button @click="handleResearch" class="research-btn">
              <i class="fas fa-sync-alt"></i> 현재 지역에서 재검색
            </button>
          </div>
        </div>
      </div>

      <!-- 검색 결과 목록 -->
      <div class="results-section">
        <div v-if="loading" class="loading">
          <i class="fas fa-spinner fa-spin"></i> 검색 중...
        </div>
        <div v-else-if="error" class="error">
          <i class="fas fa-exclamation-circle"></i> {{ error }}
        </div>
        <div v-else class="bank-list">
          <div v-for="bank in banks" :key="bank.id" class="bank-item">
            <h3>
              <i class="fas fa-university"></i>
              {{ bank.place_name }}
            </h3>
            <p class="address">
              <i class="fas fa-map-marker-alt"></i>
              <span class="label">주소:</span> 
              {{ bank.address_name }}
              <span v-if="bank.road_address_name" class="road-address">
                (도로명: {{ bank.road_address_name }})
              </span>
            </p>
            <p v-if="bank.phone" class="phone">
              <i class="fas fa-phone"></i>
              <span class="label">전화:</span> {{ bank.phone }}
            </p>
            <p class="distance" v-if="bank.distance">
              <i class="fas fa-walking"></i>
              <span class="label">거리:</span> {{ (bank.distance / 1000).toFixed(1) }}km
            </p>
            <a :href="bank.place_url" target="_blank" class="detail-link">
              <i class="fas fa-external-link-alt"></i> 상세정보 보기
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


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
      showResearchButton: false
    }
  },

  mounted() {
    // 카카오맵 스크립트 로드
    const script = document.createElement('script')
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_API_KEY}&autoload=false`
    script.async = true
    
    script.addEventListener('load', () => {
      kakao.maps.load(() => {
        this.initializeMap()
      })
    })
    
    document.head.appendChild(script)
  },

  methods: {
    initializeMap() {
      const container = document.getElementById('map')
      const options = {
        center: new kakao.maps.LatLng(37.5665, 126.9780),
        level: 3
      }
      this.map = new kakao.maps.Map(container, options)

      // 지도 이벤트 리스너
      kakao.maps.event.addListener(this.map, 'dragend', () => {
        if (this.lastSearchKeyword) {
          this.showResearchButton = true
        }
      })

      kakao.maps.event.addListener(this.map, 'zoom_changed', () => {
        if (this.lastSearchKeyword) {
          this.showResearchButton = true
        }
      })
    },

    getCurrentLocation() {
      this.loading = true
      this.error = null

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          // 위치 정보 가져오기 성공 시
          position => {
            this.currentLocation = {
              latitude: position.coords.latitude,
              longitude: position.coords.longitude
            }

            // 현재 위치로 지도 중심 이동
            const currentPosition = new kakao.maps.LatLng(
              position.coords.latitude,
              position.coords.longitude
            )
            this.map.setCenter(currentPosition)
            this.map.setLevel(3)  // 지도 확대 레벨 설정

            // 키워드가 있으면 키워드로 주변 검색, 없으면 일반 주변 검색
            if (this.searchKeyword.trim()) {
              this.searchNearbyWithKeyword()
            } else {
              this.searchNearby()
            }
          },
          // 위치 정보 가져오기 실패 시
          error => {
            this.loading = false
            this.error = '위치 정보를 가져올 수 없습니다: ' + error.message
            console.error('Geolocation error:', error)
          },
          // 옵션 설정
          {
            enableHighAccuracy: true,  // 높은 정확도
            timeout: 10000,            // 10초 타임아웃
            maximumAge: 0              // 캐시된 위치정보를 사용하지 않음
          }
        )
      } else {
        this.loading = false
        this.error = '이 브라우저에서는 위치 정보를 지원하지 않습니다.'
      }
    },

    // 키워드로 주변 검색
    async searchNearbyWithKeyword() {
      try {
        const response = await axios.get('/api/v1/locations/banks/search/', {
          params: {
            keyword: this.searchKeyword,
            latitude: this.currentLocation.latitude,
            longitude: this.currentLocation.longitude,
            radius: 1000  // 1km 반경
          }
        })
        
        if (response.data.documents) {
          this.banks = response.data.documents
          this.updateMap()
        } else {
          this.error = '주변에 검색 결과가 없습니다.'
        }
      } catch (error) {
        console.error('Error:', error)
        this.error = '검색 중 오류가 발생했습니다.'
      } finally {
        this.loading = false
      }
    },

    // 일반 주변 검색
    async searchNearby() {
      try {
        const response = await axios.get('/api/v1/locations/banks/nearby/', {
          params: {
            latitude: this.currentLocation.latitude,
            longitude: this.currentLocation.longitude,
            radius: 1000  // 1km 반경
          }
        })

        if (response.data.banks) {  // response.data.banks로 수정
          this.banks = response.data.banks
          this.updateMap()
        } else {
          this.error = '주변에 은행이 없습니다.'
        }
      } catch (error) {
        console.error('Error:', error)
        this.error = '은행 검색 중 오류가 발생했습니다.'
      } finally {
        this.loading = false
      }
    },

    // async searchNearby() {
    //   try {
    //     const response = await axios.get('/api/v1/locations/banks/nearby/', {
    //       params: {
    //         latitude: this.currentLocation.latitude,
    //         longitude: this.currentLocation.longitude,
    //         radius: 1000
    //       }
    //     })
        
    //     // response.data.banks로 수정
    //     if (response.data.banks && response.data.banks.length > 0) {
    //       this.banks = response.data.banks
    //       this.updateMap()
    //     } else {
    //       this.error = '주변에 은행이 없습니다.'
    //     }
    //   } catch (error) {
    //     console.error('Error:', error)
    //     this.error = '은행 검색 중 오류가 발생했습니다.'
    //   } finally {
    //     this.loading = false
    //   }
    // },

    async searchByKeyword() {
      if (!this.searchKeyword.trim()) {
        this.error = '검색어를 입력해주세요.'
        return
      }

      this.loading = true
      this.error = null
      this.lastSearchKeyword = this.searchKeyword

      try {
        const response = await axios.get('/api/v1/locations/banks/search/', {
          params: { 
            keyword: this.searchKeyword 
          }
        })
        
        if (response.data.documents) {
          this.banks = response.data.documents
          this.updateMap()
          this.showResearchButton = false
        } else {
          this.error = '검색 결과가 없습니다.'
        }
      } catch (error) {
        console.error('Error:', error)
        this.error = '검색 중 오류가 발생했습니다.'
      } finally {
        this.loading = false
      }
    },

    // async searchNearbyWithKeyword() {
    //   try {
    //     const response = await axios.get('/api/v1/locations/banks/search/', {
    //       params: {
    //         keyword: this.searchKeyword,
    //         latitude: this.currentLocation.latitude,
    //         longitude: this.currentLocation.longitude,
    //         radius: 1000
    //       }
    //     })
        
    //     if (response.data.documents && response.data.documents.length > 0) {
    //       this.banks = response.data.documents
    //       this.updateMap()
    //     } else {
    //       this.error = '주변에 검색 결과가 없습니다.'
    //     }
    //   } catch (error) {
    //     console.error('Error:', error)
    //     this.error = '검색 중 오류가 발생했습니다.'
    //   } finally {
    //     this.loading = false
    //   }
    // },

    async handleResearch() {
      const center = this.map.getCenter()
      this.loading = true
      this.error = null

      try {
        const response = await axios.get('/api/v1/locations/banks/search/', {
          params: {
            keyword: this.lastSearchKeyword,
            latitude: center.getLat(),
            longitude: center.getLng(),
            radius: 5000
          }
        })
        
        if (response.data.documents) {
          this.banks = response.data.documents
          this.updateMarkersOnly()
          this.showResearchButton = false
        } else {
          this.error = '검색 결과가 없습니다.'
        }
      } catch (error) {
        console.error('Error:', error)
        this.error = '검색 중 오류가 발생했습니다.'
      } finally {
        this.loading = false
      }
    },

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
      this.markers.forEach(marker => marker.setMap(null))
      this.markers = []
    },

    createMarker(position, bank) {
      const marker = new kakao.maps.Marker({ position })
      marker.setMap(this.map)
      this.markers.push(marker)

      const infowindow = new kakao.maps.InfoWindow({
        content: `
          <div style="padding:10px;width:250px;font-size:12px;">
            <h4 style="margin:0 0 5px;font-size:14px;color:#333;">${bank.place_name}</h4>
            ${bank.phone ? 
              `<p style="margin:5px 0;color:#666;">
                <span style="color:#2196F3;">☎</span> ${bank.phone}
              </p>` : ''
            }
            <p style="margin:5px 0;color:#666;">
              <span style="color:#4CAF50;">📍</span> ${bank.address_name}
            </p>
            ${bank.road_address_name ? 
              `<p style="margin:5px 0;color:#888;font-size:11px;">
                (도로명: ${bank.road_address_name})
              </p>` : ''
            }
            ${bank.distance ? 
              `<p style="margin:5px 0;color:#666;">
                <span style="color:#FF9800;">🚶</span> ${(bank.distance / 1000).toFixed(1)}km
              </p>` : ''
            }
          </div>
        `
        , removable: true  // 닫기 버튼 표시
      })

      kakao.maps.event.addListener(marker, 'click', () => {
        infowindow.open(this.map, marker)
      })
      return marker
    }
  }
}
</script>

<style scoped>
.bank-search {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.search-form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-box {
  flex: 1;
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.search-btn {
  background-color: #4CAF50;
  color: white;
}

.search-btn:hover {
  background-color: #45a049;
  transform: translateY(-1px);
}

.location-btn {
  background-color: #2196F3;
  color: white;
}

.location-btn:hover {
  background-color: #1976D2;
  transform: translateY(-1px);
}

.map-container {
  position: relative;
  height: 400px;
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #ddd;
}

.research-button-container {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
}

.research-btn {
  background-color: white;
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  font-size: 14px;
  border: none;
}

.research-btn:hover {
  background-color: #f5f5f5;
  transform: translateY(-1px);
}

.research-btn i {
  margin-right: 5px;
}

.bank-list {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.bank-item {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.bank-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.bank-item h3 {
  margin: 0 0 10px 0;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

.label {
  font-weight: bold;
  color: #666;
}

.address, .phone, .distance {
  margin: 5px 0;
  font-size: 14px;
  color: #666;
  display: flex;
  align-items: center;
  gap: 8px;
}

.road-address {
  color: #888;
  font-size: 13px;
  margin-left: 8px;
}

.detail-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  margin-top: 10px;
  color: #2196F3;
  text-decoration: none;
  font-size: 14px;
}

.detail-link:hover {
  text-decoration: underline;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.error {
  text-align: center;
  padding: 20px;
  color: #f44336;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .bank-list {
    grid-template-columns: 1fr;
  }

  .search-form {
    flex-direction: column;
  }

  .location-btn {
    width: 100%;
  }
}
</style>