<template>
  <Layout>
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Загрузка товара...</p>
    </div>
    
    <div v-else-if="part" class="product-page">
      <!-- Хлебные крошки -->
      <div class="breadcrumb">
        <router-link to="/" class="breadcrumb-link">Главная</router-link>
        <span class="breadcrumb-separator">/</span>
        <router-link to="/catalog" class="breadcrumb-link">Каталог</router-link>
        <span class="breadcrumb-separator">/</span>
        <span class="breadcrumb-current">{{ part.name }}</span>
      </div>

      <div class="product-card">
        <!-- Изображение -->
        <div class="product-image-section">
          <div class="image-frame-wrapper">
            <div class="glowing-frame"></div>
            <img 
              v-if="part.img_path" 
              :src="getImageUrl(part.img_path)" 
              :alt="part.name"
              class="product-image"
            >
            <div v-else class="image-placeholder">
              <i class="fa-solid fa-image"></i>
            </div>
          </div>
        </div>

        <!-- Информация -->
        <div class="product-info-section">
          <div class="product-header">
            <span class="category-badge">{{ part.category_name }}</span>
            <h1 class="product-title">{{ part.name }}</h1>
            <p class="product-article">Артикул: <span class="article-value">{{ part.article }}</span></p>
          </div>

          <div class="manufacturer-info">
            <strong>Производитель:</strong> 
            <span>{{ part.manufacturer_name || 'Не указан' }}</span>
            <span v-if="part.country" class="country">({{ part.country }})</span>
          </div>

          <div class="price-block">
            <div class="price-main">
              <span class="price-label">Цена:</span>
              <span class="price-value">{{ formatPrice(part.price) }} ₽</span>
            </div>
            <div class="stock-info" :class="{ 'low-stock': part.quantity < 10 }">
              <i class="fa-solid fa-warehouse"></i>
              <span>В наличии: {{ part.quantity }} шт.</span>
            </div>
          </div>

          <button class="add-to-cart-button">
            <i class="fa-solid fa-cart-plus"></i>
            Добавить в корзину
          </button>

          <div class="product-details">
            <h3 class="details-title">Описание и характеристики</h3>
            <div class="description" v-html="part.description || 'Описание отсутствует'"></div>
            
            <div v-if="part.compatible_cars" class="compatibility-section">
              <h4>Совместимость:</h4>
              <p class="compatibility-list">{{ part.compatible_cars }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import Layout from './okno.vue';

const API_BASE = 'http://localhost:5000';
const route = useRoute();
const part = ref(null);
const loading = ref(true);

onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/api/part/${route.params.id}`);
    if (res.ok) {
      part.value = await res.json();
    }
  } catch (error) {
    console.error('Ошибка загрузки товара:', error);
  } finally {
    loading.value = false;
  }
});

const formatPrice = (price) => {
  return Number(price).toLocaleString('ru-RU');
};

const getImageUrl = (path) => {
  return path ? `${API_BASE}/images/${path}` : '';
};
</script>

<style scoped>
.product-page {
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

.product-card {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 40px;
  background: rgba(20, 20, 30, 0.8);
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.product-image-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-frame-wrapper {
  position: relative;
  width: 100%;
  max-width: 400px;
  aspect-ratio: 1;
  padding: 4px;
  background: linear-gradient(72deg, #01f2ff, #000000, #0720f7);
  background-size: 200% 200%;
  animation: glowing-border 4s linear infinite;
  border-radius: 12px;
  overflow: hidden;
}

.glowing-frame {
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

.product-image {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #000;
  border-radius: 8px;
}

.image-placeholder {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
  color: #333;
  font-size: 100px;
  border-radius: 8px;
}

.product-info-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.product-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 20px;
}

.category-badge {
  display: inline-block;
  background: rgba(52, 152, 219, 0.2);
  color: #3498db;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  margin-bottom: 12px;
}

.product-title {
  font-size: 32px;
  font-weight: bold;
  color: #fff;
  margin: 0 0 12px;
}

.product-article {
  font-size: 14px;
  color: #888;
}

.article-value {
  font-family: monospace;
  color: #3498db;
  background: rgba(52, 152, 219, 0.1);
  padding: 2px 8px;
  border-radius: 4px;
}

.manufacturer-info {
  font-size: 15px;
  color: #aaa;
}

.manufacturer-info strong {
  color: #fff;
}

.price-block {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid rgba(52, 152, 219, 0.2);
}

.price-main {
  display: flex;
  align-items: baseline;
  gap: 16px;
  margin-bottom: 12px;
}

.price-label {
  font-size: 18px;
  color: #888;
}

.price-value {
  font-size: 42px;
  font-weight: bold;
  color: #3498db;
}

.stock-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #2ecc71;
}

.stock-info.low-stock {
  color: #e74c3c;
}

.add-to-cart-button {
  width: 100%;
  padding: 18px 32px;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);
}

.add-to-cart-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(52, 152, 219, 0.6);
}

.product-details {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  padding: 24px;
}

.details-title {
  font-size: 20px;
  color: #fff;
  margin: 0 0 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.description {
  color: #aaa;
  line-height: 1.8;
}

.compatibility-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.compatibility-section h4 {
  color: #fff;
  font-size: 16px;
  margin: 0 0 12px;
}

.compatibility-list {
  color: #888;
  font-size: 14px;
}

@media (max-width: 968px) {
  .product-card {
    grid-template-columns: 1fr;
  }
}
</style>