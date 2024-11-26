<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'

// 상태 관리
const searchKeyword = ref('')
const banks = ref([])
const loading = ref(false)
const error = ref(null)
const map = ref(null)
const markers = ref([])
const currentLocation = ref({ latitude: null, longitude: null })
const lastSearchKeyword = ref('')
const showResearchButton = ref(false)
const showSidebar = ref(localStorage.getItem('showSidebar') !== 'false')
const currentInfowindow = ref(null)
const activeMarker = ref(null)
const infowindows = ref([])

const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371000; // 지구의 반지름 (미터 단위)
  const φ1 = lat1 * Math.PI/180;
  const φ2 = lat2 * Math.PI/180;
  const Δφ = (lat2-lat1) * Math.PI/180;
  const Δλ = (lon2-lon1) * Math.PI/180;

  const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
          Math.cos(φ1) * Math.cos(φ2) *
          Math.sin(Δλ/2) * Math.sin(Δλ/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

  return R * c; // 미터 단위로 반환
}
// 지도 초기화
const initializeMap = () => {
  try {
    const container = document.getElementById('map')
    if (!container) {
      console.error('Map container not found')
      return
    }
    
    const options = {
      center: new kakao.maps.LatLng(37.5665, 126.9780),
      level: 3
    }
    map.value = new kakao.maps.Map(container, options)
    
    initializeMapEvents()
  } catch (error) {
    console.error('Map initialization error:', error)
  }
}
const toggleSidebar = () => {
  showSidebar.value = !showSidebar.value
  localStorage.setItem('showSidebar', showSidebar.value)
}

const initializeMapEvents = () => {
  kakao.maps.event.addListener(map.value, 'dragend', showResearchButtonIfNeeded)
  kakao.maps.event.addListener(map.value, 'zoom_changed', showResearchButtonIfNeeded)
}

const showResearchButtonIfNeeded = () => {
  if (lastSearchKeyword.value || (currentLocation.value.latitude && currentLocation.value.longitude)) {
    showResearchButton.value = true
  }
}

const debounce = (func, wait) => {
  let timeout
  return (...args) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

const getCurrentLocation = async () => {
  console.log('getCurrentLocation')
  loading.value = true
  error.value = null
  
  // 1. 브라우저 지원 확인
  if (!navigator.geolocation) {
    error.value = '이 브라우저에서는 위치 정보를 지원하지 않습니다.'
    loading.value = false
    return
  }

  try {
    // 2. 위치 정보 가져오기 옵션 설정
    const options = {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0
    }
    
    // 3. Promise로 위치 정보 요청
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject, options)
    })
    
    // 4. 위치 정보 저장
    currentLocation.value = {
      latitude: position.coords.latitude,
      longitude: position.coords.longitude
    }
    
    // 5. 지도 중심 이동
    const currentPosition = new kakao.maps.LatLng(
      currentLocation.value.latitude,
      currentLocation.value.longitude
    )
    map.value.setCenter(currentPosition)
    map.value.setLevel(3)
    
    // 6. 검색 실행
    await searchNearby()
    
  } catch (err) {
    // 7. 에러 처리 개선
    if (err.code === 1) {
      error.value = '위치 정보 액세스가 거부되었습니다. 브라우저의 위치 정보 권한을 확인해주세요.'
    } else if (err.code === 2) {
      error.value = '위치 정보를 가져올 수 없습니다. 네트워크 연결을 확인해주세요.'
    } else if (err.code === 3) {
      error.value = '위치 정보 요청 시간이 초과되었습니다. 다시 시도해주세요.'
    } else {
      error.value = '위치 정보를 가져오는 중 오류가 발생했습니다.'
    }
    console.error('Geolocation error:', err)
  } finally {
    loading.value = false
  }
}


const searchByKeywordAndLocation = async () => {
  console.log('searchByKeywordAndLocation')
  loading.value = true
  error.value = null

  try {
    const bounds = map.value.getBounds()
    const sw = bounds.getSouthWest()
    const ne = bounds.getNorthEast()

    const response = await axios.get('/api/v1/locations/banks/search/', {
      params: {
        keyword: searchKeyword.value,
        sw_lat: sw.getLat(),
        sw_lng: sw.getLng(),
        ne_lat: ne.getLat(),
        ne_lng: ne.getLng()
      }
    })

    if (response.data.documents?.length > 0) {
      banks.value = response.data.documents
      updateMap()
      showResearchButton.value = false
      lastSearchKeyword.value = searchKeyword.value
    } else {
      error.value = '현재 위치 주변에 검색 결과가 없습니다.'
      banks.value = []
    }
  } catch (error) {
    console.error('Error:', error)
    error.value = '검색 중 오류가 발생했습니다.'
    banks.value = []
  } finally {
    loading.value = false
  }
}


const searchNearby = async () => {
  loading.value = true
  error.value = null
  
  try {
    const params = {
      latitude: currentLocation.value.latitude,
      longitude: currentLocation.value.longitude,
      radius: 1000
    }

    // 키워드가 있는 경우에만 params에 추가
    if (searchKeyword.value.trim()) {
      params.keyword = searchKeyword.value
    }

    const response = await axios.get('/api/v1/locations/banks/nearby/', {
      params: params
    })

    if (response.data?.banks?.length > 0) {
      banks.value = response.data.banks
      updateMap()
      showResearchButton.value = false
    } else {
      error.value = '주변에 검색 결과가 없습니다.'
      banks.value = []
    }
  } catch (error) {
    console.error('Error:', error)
    error.value = error.response?.data?.message || '검색 중 오류가 발생했습니다.'
    banks.value = []
  } finally {
    loading.value = false
  }
}

const searchByKeyword = async () => {
  console.log('searchByKeyword')
  if (!searchKeyword.value.trim()) {
    error.value = '검색어를 입력해주세요.'
    return
  }

  loading.value = true
  error.value = null
  lastSearchKeyword.value = searchKeyword.value
  
  try {
    const response = await axios.get('/api/v1/locations/banks/search/', {
      params: {
        keyword: searchKeyword.value
      }
    })

    if (response.data?.documents?.length > 0) {
      banks.value = response.data.documents
      updateMap()
      showResearchButton.value = false
    } else {
      error.value = '검색 결과가 없습니다.'
      banks.value = []
    }
  } catch (error) {
    console.error('Search Error:', error)
    error.value = error.response?.data?.message || error.message || '검색 중 오류가 발생했습니다.'
    banks.value = []
  } finally {
    loading.value = false
  }
}

const handleResearch = async () => {
  if (loading.value) return
  
  const bounds = map.value.getBounds()
  const sw = bounds.getSouthWest()
  const ne = bounds.getNorthEast()
  
  loading.value = true
  error.value = null
  
  try {
    if (lastSearchKeyword.value && lastSearchKeyword.value.trim()) {
      // 이전 키워드가 있는 경우의 로직은 유지
      const response = await axios.get('/api/v1/locations/banks/search/', {
        params: {
          keyword: lastSearchKeyword.value,
          sw_lat: sw.getLat(),
          sw_lng: sw.getLng(),
          ne_lat: ne.getLat(),
          ne_lng: ne.getLng()
        }
      })

      if (response.data?.documents?.length > 0) {
        banks.value = response.data.documents
        updateMarkersOnly()
        showResearchButton.value = false
      } else {
        error.value = '이 지역에 검색 결과가 없습니다.'
        banks.value = []
      }
    } else {
      // 이전 키워드가 없는 경우 "은행" 키워드로 영역 검색
      const response = await axios.get('/api/v1/locations/banks/search/', {
        params: {
          keyword: '은행',
          sw_lat: sw.getLat(),
          sw_lng: sw.getLng(),
          ne_lat: ne.getLat(),
          ne_lng: ne.getLng()
        }
      })

      if (response.data?.documents?.length > 0) {
        banks.value = response.data.documents
        updateMarkersOnly()
        showResearchButton.value = false
      } else {
        error.value = '이 지역에 은행이 없습니다.'
        banks.value = []
      }
    }
  } catch (error) {
    console.error('Error:', error)
    error.value = error.response?.data?.message || '검색 중 오류가 발생했습니다.'
    banks.value = []
  } finally {
    loading.value = false
  }
}


const updateMap = () => {
  console.log('updateMap')
  if (!map.value || !banks.value.length) return
  clearMarkers()
  const bounds = new kakao.maps.LatLngBounds()
  banks.value.forEach(bank => {
    const position = new kakao.maps.LatLng(bank.y, bank.x)
    const marker = createMarker(position, bank)
    bounds.extend(position)
  })
  map.value.setBounds(bounds)
}

const updateMarkersOnly = () => {
  if (!map.value || !banks.value.length) return
  clearMarkers()
  banks.value.forEach(bank => {
    const position = new kakao.maps.LatLng(bank.y, bank.x)
    createMarker(position, bank)
  })
}

// 인포윈도우 관리 함수들
const infowindowController = {
  open(infowindow, marker) {
    try {
      if (currentInfowindow.value) {
        currentInfowindow.value.close()
        if (activeMarker.value === marker) {
          this.clear()
          return false
        }
      }
      
      infowindow.open(map.value, marker)
      currentInfowindow.value = infowindow
      activeMarker.value = marker
      infowindows.value.push(infowindow)
      return true
    } catch (error) {
      console.error('InfoWindow open error:', error)
      return false
    }
  },
  
  clear() {
    try {
      currentInfowindow.value = null
      activeMarker.value = null
    } catch (error) {
      console.error('InfoWindow clear error:', error)
    }
  },
  
  closeAll() {
    try {
      infowindows.value.forEach(info => {
        if (info && typeof info.close === 'function') {
          info.close()
        }
      })
      infowindows.value = []
      this.clear()
    } catch (error) {
      console.error('InfoWindow closeAll error:', error)
    }
  }
}

const createMarker = (position, bank) => {
  try {
    const marker = new kakao.maps.Marker({ position })
    marker.setMap(map.value)
    markers.value.push(marker)

    const infowindow = new kakao.maps.InfoWindow({
      content: createInfoWindowContent(bank),
      removable: true
    })

    kakao.maps.event.addListener(marker, 'click', () => {
      const isOpened = infowindowController.open(infowindow, marker)
      if (isOpened) {
        const bankCard = document.querySelector(`[data-bank-id="${bank.id}"]`)
        if (bankCard) {
          bankCard.scrollIntoView({ behavior: 'smooth' })
        }
      }
    })

    kakao.maps.event.addListener(infowindow, 'closeclick', () => {
      infowindowController.clear()
    })

    return marker
  } catch (error) {
    console.error('Marker creation error:', error)
    return null
  }
}

const clearMarkers = () => {
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []
  infowindowController.closeAll()
}

const moveToBank = (bank) => {
  const position = new kakao.maps.LatLng(bank.y, bank.x)
  map.value.setCenter(position)
  map.value.setLevel(3)
  
  infowindowController.closeAll()

  setTimeout(() => {
    const targetMarker = markers.value.find(marker => {
      const markerPos = marker.getPosition()
      return Math.abs(markerPos.getLat() - bank.y) < 0.0000001 
        && Math.abs(markerPos.getLng() - bank.x) < 0.0000001
    })

    if (targetMarker) {
      const infowindow = new kakao.maps.InfoWindow({
        content: createInfoWindowContent(bank),
        removable: true
      })
      
      kakao.maps.event.addListener(infowindow, 'closeclick', () => {
        infowindowController.clear()
      })
      
      infowindowController.open(infowindow, targetMarker)
    }
  }, 100)
}

const createInfoWindowContent = (bank) => {
  return `
    <div style="padding:10px;width:250px;font-size:12px;">
      <h4 style="margin:0 0 5px;font-size:14px;color:#333;">${bank.place_name}</h4>
      ${bank.phone ? `<p style="margin:5px 0;color:#666;"><span style="color:#2196F3;">☎</span> ${bank.phone}</p>` : ''}
      <p style="margin:5px 0;color:#666;"><span style="color:#4CAF50;">📍</span> ${bank.address_name}</p>
      ${bank.road_address_name ? `<p style="margin:5px 0;color:#888;font-size:11px;">(도로명: ${bank.road_address_name})</p>` : ''}
      ${bank.distance ? `<p style="margin:5px 0;color:#666;"><span style="color:#FF9800;">🚶</span> ${(bank.distance / 1000).toFixed(1)}km</p>` : ''}
    </div>
  `
}

// searchKeyword가 변경될 때 실행될 watch 함수 추가
watch(searchKeyword, (newValue) => {
  if (!newValue.trim()) {
    lastSearchKeyword.value = ''
  }
})

// 라이프사이클 훅
onMounted(() => {
  const script = document.createElement('script')
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_API_KEY}&autoload=false`
  script.async = true
  script.addEventListener('load', () => {
    kakao.maps.load(() => {
      initializeMap()
      initializeMapEvents()
    })
  })   
  document.head.appendChild(script)
})

onBeforeUnmount(() => {
  clearMarkers()
  if (map.value) {
    kakao.maps.event.removeListener(map.value, 'dragend')
    kakao.maps.event.removeListener(map.value, 'zoom_changed')
  }
})
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
@font-face {
  font-family: 'JalnanFont';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_four@1.2/JalnanOTF00.woff') format('woff');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'GowunDodum-Regular';
  src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/GowunDodum-Regular.woff') format('woff');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

.bank-search {
  max-width: 1400px;
  margin: 24px auto;
  padding: 32px;
  background-color: #fffefb;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(115, 85, 60, 0.12);
  height: 90vh;
}

.title {
  font-family: 'JalnanFont';
  color: #73553C;
  text-align: center;
  margin-bottom: 16px;
  font-size: 32px;
  line-height: 1.4;
}

.search-section {
  background-color: #FEF0AC;
  border-radius: 8px;
  padding: 12px;
  border: 1px solid #FDE49B;
  margin-bottom: 10px;
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.search-box {
  display: flex;
  gap: 8px;
  align-items: center;
}

input {
  flex: 1;
  padding: 0 16px;
  border: 1px solid #FDE49B;
  border-radius: 8px;
  font-family: 'GowunDodum-Regular';
  font-size: 14px;
  background-color: #FFFEFB;
  color: #73553C;
  transition: all 0.2s ease;
  height: 40px;
  line-height: 40px;
  box-sizing: border-box;
}

.location-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-family: 'GowunDodum-Regular';
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 40px;
}

.search-btn {
  padding: 0 16px;
  border: none;
  border-radius: 8px;
  font-family: 'GowunDodum-Regular';
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 40px;
  line-height: 40px;
  background-color: #73553C;
  color: #FFFEFB;
  box-sizing: border-box;
}

.search-btn {
  background-color: #73553C;
  color: #FFFEFB;
}

.location-btn {
  background-color: #3D0F0E;
  color: #FFFEFB;
  width: 100%;
}

.results-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
  height: calc(100vh - 200px); /* 상단 여백과 검색창 높이를 고려한 계산 */
  overflow-y: auto; /* 세로 스크롤 추가 */
  scrollbar-width: thin; /* Firefox를 위한 스크롤바 스타일 */
  scrollbar-color: #73553C #f5f5f5; /* Firefox를 위한 스크롤바 색상 */
}

/* Chrome, Safari, Edge를 위한 스크롤바 스타일 */
.results-section::-webkit-scrollbar {
  width: 8px;
}

.results-section::-webkit-scrollbar-track {
  background: #f5f5f5;
  border-radius: 4px;
}

.results-section::-webkit-scrollbar-thumb {
  background: #73553C;
  border-radius: 4px;
}

.results-section::-webkit-scrollbar-thumb:hover {
  background: #5a4230;
}

.content-wrapper {
  display: flex;
  gap: 32px;
  margin: 0 auto;
  padding: 32px;
  background: #FFFEFB;
  border-radius: 16px;
  border: 3px solid #FDE49B;
  height: calc(90vh - 120px);
}


.left-sidebar {
  width: 350px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  flex-shrink: 0;
}


.map-section {
  flex: 2;
  background-color: #FEF0AC;
  border-radius: 12px;
  /* padding: 2px; */
  border: 1px solid #FDE49B;
  position: relative;
  min-width: 0;
}

.map-container {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  border: 1px solid #FDE49B;
  box-shadow: 0 0 0 1px rgba(253, 228, 155, 0.5);
  overflow: hidden;
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
  font-family: 'GowunDodum-Regular', sans-serif;
}

.results-count {
  padding: 0.5rem;
  margin: 0;
  font-family: 'GowunDodum-Regular', sans-serif;
  text-align: left;
}

.bank-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
  max-height: calc(100vh - 250px); /* 상단 여백, 검색창, 결과 카운트 등을 고려한 높이 */
  width: 100%;
}


.bank-card {
  margin-bottom: 0.8rem;
  background: #FFFEFB;
  border: 1px solid #FDE49B;
  border-radius: 8px;
  padding: 0.8rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: all 0.2s ease;
  text-align: left; /* 전체 카드의 텍스트를 왼쪽 정렬 */
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

.bank-header h3 {
  margin: 0;
  text-align: left;
  flex: 1; /* h3가 가능한 공간을 모두 차지하도록 설정 */
}

.bank-info {
  padding: 0.2rem 0;
  color: #3D0F0E;
  font-size: 0.75rem;
  line-height: 1.3;
  text-align: left;
}

.bank-info p {
  margin: 0.2rem 0;
  text-align: left;
}

.distance-badge {
  background: #FEF0AC;
  color: #73553C;
  padding: 0.25rem 0.5rem;
  border-radius: 16px;
  font-size: 0.85rem;
  margin-left: auto;
  flex-shrink: 0; /* 거리 배지가 줄어들지 않도록 설정 */
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  color: #73553C;
}

.empty-state-icon {
  font-size: 48px;
  color: #FDE49B;
}

.empty-state-text {
  font-family: 'GowunDodum-Regular';
  font-size: 14px;
  line-height: 1.5;
}

.empty-state-tips {
  font-size: 12px;
  color: #666;
  margin-top: 8px;
}

.status-message.loading {
  font-family: 'GowunDodum-Regular', sans-serif;
  color: #3498db;
  padding: 16px;
  border-radius: 8px;
  background-color: #f7fbfe;
  border: 1px solid #d4e9f7;
  margin: 16px 0;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
}

.status-message.loading i {
  font-size: 18px;
  animation: spin 1s infinite linear;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1440px) {
  .bank-search {
    margin: 16px;
    padding: 24px;
  }
  
  .content-wrapper {
    padding: 24px;
    gap: 24px;
  }

  .title {
    font-size: 28px;
  }
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

  .search-btn, .location-btn {
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

.status-message.error {
  font-family: 'GowunDodum-Regular', sans-serif;
  color: #e74c3c;
  padding: 16px;
  border-radius: 8px;
  background-color: #fef5f5;
  border: 1px solid #fadbd8;
  margin: 16px 0;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
}

.status-message.error i {
  font-size: 18px;
}

</style>
