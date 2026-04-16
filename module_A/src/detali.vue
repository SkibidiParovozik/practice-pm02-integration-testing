<template>
  <Layout>
    <div class="catalog-page">
      <!-- Хлебные крошки -->
      <div class="breadcrumb">
        <router-link to="/" class="breadcrumb-link">Главная</router-link>
        <span class="breadcrumb-separator">/</span>
        <span class="breadcrumb-current">{{ pageTitle }}</span>
      </div>

      <h1 class="page-title">{{ pageTitle }}</h1>

      <!-- Загрузка -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Загрузка запчастей...</p>
      </div>

      <!-- Нет товаров -->
      <div v-else-if="parts.length === 0" class="empty-state">
        <i class="fa-solid fa-inbox"></i>
        <p>Запчасти не найдены</p>
      </div>

      <!-- Сетка запчастей -->
      <div v-else class="parts-grid">
        <div 
          v-for="part in parts" 
          :key="part.id"
          @click="goToPart(part.id)"
          class="part-card clickable"
        >
          <div class="part-image-container">
            <img 
              v-if="part.img_path" 
              :src="getImageUrl(part.img_path)" 
              :alt="part.name"
              class="part-image"
            >
            <div v-else class="part-placeholder">
              <i class="fa-solid fa-image"></i>
            </div>
            <div class="animated-frame"></div>
          </div>
          
          <div class="part-info">
            <p class="part-manufacturer">{{ part.manufacturer_name || 'Производитель' }}</p>
            <h3 class="part-name">{{ part.name }}</h3>
            <p class="part-article">Артикул: {{ part.article }}</p>
            
            <div class="part-footer">
              <span class="part-price">{{ formatPrice(part.price) }} ₽</span>
              <span class="part-quantity" :class="{ 'low-stock': part.quantity < 10 }">
                {{ part.quantity }} шт.
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Layout from './okno.vue';

const API_BASE = 'http://localhost:5000';
const route = useRoute();
const router = useRouter();
const parts = ref([]);
const loading = ref(true);

const pageTitle = computed(() => {
  if (route.params.type === 'category') {
    return `Категория #${route.params.id}`;
  } else if (route.params.type === 'car') {
    return `Запчасти для автомобиля #${route.params.id}`;
  }
  return 'Каталог запчастей';
});

onMounted(async () => {
  loading.value = true;
  let url = '';
  
  console.log('Params:', route.params);
  
  if (route.params.type === 'category') {
    url = `${API_BASE}/api/parts?category_id=${route.params.id}`;
  } else if (route.params.type === 'car') {
    url = `${API_BASE}/api/parts?car_id=${route.params.id}`;
  }
  
  console.log('Request URL:', url);

  try {
    const res = await fetch(url);
    parts.value = await res.json();
    console.log('Received parts:', parts.value);
  } catch (error) {
    console.error('Ошибка загрузки запчастей:', error);
  } finally {
    loading.value = false;
  }
});

const goToPart = (id) => {
  router.push(`/part/${id}`);
};

const formatPrice = (price) => {
  return Number(price).toLocaleString('ru-RU');
};

const getImageUrl = (path) => {
  return path ? `${API_BASE}/images/${path}` : '';
};
</script>

<style scoped>
.catalog-page {
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
}

.breadcrumb {
  margin-bottom: 20px;
  font-size: 14px;
  color: #888;
}

.breadcrumb-link {
  color: #3498db;
  text-decoration: none;
  transition: color 0.3s;
}

.breadcrumb-link:hover {
  color: #5dade2;
}

.breadcrumb-separator {
  margin: 0 10px;
  color: #555;
}

.breadcrumb-current {
  color: #aaa;
}

.page-title {
  font-size: 32px;
  font-weight: bold;
  color: #fff;
  margin-bottom: 40px;
  text-shadow: 0 0 20px rgba(52, 152, 219, 0.5);
}

.loading-container {
  text-align: center;
  padding: 100px 20px;
  color: #888;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(52, 152, 219, 0.2);
  border-top-color: #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 100px 20px;
  color: #666;
}

.empty-state i {
  font-size: 80px;
  margin-bottom: 20px;
  opacity: 0.3;
}

.parts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
}

.part-card {
  position: relative;
  background: rgba(20, 20, 30, 0.8);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.part-card.clickable:hover {
  transform: scale(1.05) translateY(-5px);
  box-shadow: 0 20px 40px rgba(52, 152, 219, 0.3);
}

.part-image-container {
  position: relative;
  width: 100%;
  height: 220px;
  background: #000;
  padding: 3px;
  overflow: hidden;
}

.animated-frame {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(72deg, #01f2ff, #000000, #0720f7);
  background-size: 200% 200%;
  animation: glowing-border 4s linear infinite;
  z-index: 0;
}

@keyframes glowing-border {
  0% { box-shadow: 0 0 10px #00f2ff; background-position: 0% 0%; }
  50% { box-shadow: 0 0 15px #ff00ff; background-position: 100% 100%; }
  100% { box-shadow: 0 0 10px #00f2ff; background-position: 0% 0%; }
}

.part-image {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.part-placeholder {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
  color: #333;
  font-size: 60px;
}

.part-info {
  padding: 20px;
  color: #fff;
}

.part-manufacturer {
  font-size: 12px;
  color: #888;
  margin-bottom: 8px;
}

.part-name {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin: 0 0 10px;
  min-height: 45px;
}

.part-article {
  font-size: 12px;
  color: #666;
  margin-bottom: 15px;
  font-family: monospace;
}

.part-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.part-price {
  font-size: 22px;
  font-weight: bold;
  color: #3498db;
}

.part-quantity {
  font-size: 13px;
  color: #2ecc71;
  background: rgba(46, 204, 113, 0.1);
  padding: 4px 10px;
  border-radius: 12px;
}

.part-quantity.low-stock {
  color: #e74c3c;
  background: rgba(231, 76, 60, 0.1);
}
</style>
