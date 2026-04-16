<template>
  <Layout>
    <div class="home-page">
      <h1 class="main-title">Каталоги запчастей и товаров</h1>
      
      <!-- Секция: Подбор по автомобилю -->
      <section class="section">
        <h2 class="section-title">
          Подбор по автомобилю
          <i class="fa-solid fa-chevron-right"></i>
        </h2>
        <div class="tiles-grid">
          <div 
            v-for="car in cars" 
            :key="car.id"
            @click="selectCar(car.id)"
            class="tile-item clickable"
          >
            <div class="tile-image-container">
              <img 
                v-if="car.car_img_path" 
                :src="getImageUrl(car.car_img_path)" 
                :alt="`${car.brand} ${car.model}`"
                class="tile-image"
              >
              <div v-else class="tile-placeholder">
                <i class="fa-solid fa-car"></i>
              </div>
              <div class="animated-frame"></div>
            </div>
            <h3 class="tile-title">{{ car.brand }} {{ car.model }}</h3>
            <p class="tile-years">{{ car.year_from }} - {{ car.year_to || 'н.в.' }}</p>
          </div>
        </div>
      </section>

      <!-- Секция: Категории запчастей -->
      <section class="section">
        <h2 class="section-title">
          Категории запчастей
          <i class="fa-solid fa-chevron-right"></i>
        </h2>
        <div class="tiles-grid">
          <div 
            v-for="cat in categories" 
            :key="cat.id"
            @click="selectCategory(cat.id)"
            class="tile-item clickable"
          >
            <div class="tile-image-container">
              <img 
                v-if="cat.category_img_path" 
                :src="getImageUrl(cat.category_img_path)" 
                :alt="cat.name"
                class="tile-image"
              >
              <div v-else class="tile-placeholder">
                <i class="fa-solid fa-box-open"></i>
              </div>
              <div class="animated-frame"></div>
            </div>
            <h3 class="tile-title">{{ cat.name }}</h3>
            <p class="tile-description">{{ cat.description }}</p>
          </div>
        </div>
      </section>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Layout from './okno.vue';

const API_BASE = 'http://localhost:5000';
const router = useRouter();
const categories = ref([]);
const cars = ref([]);

onMounted(async () => {
  try {
    const catRes = await fetch(`${API_BASE}/api/categories`);
    categories.value = await catRes.json();

    const carRes = await fetch(`${API_BASE}/api/cars`);
    cars.value = await carRes.json();
  } catch (error) {
    console.error('Ошибка загрузки данных:', error);
  }
});

const selectCategory = (id) => {
  console.log('Клик по категории:', id);
  const path = `/catalog/category/${id}`;
  console.log('➡️ Переход по:', path);
  router.push(path);
};

const selectCar = (id) => {
  router.push(`/catalog/car/${id}`);
};

const getImageUrl = (path) => {
  return path ? `${API_BASE}/images/${path}` : '';
};
</script>

<style scoped>
.home-page {
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
}

.main-title {
  font-size: 36px;
  font-weight: bold;
  color: #fff;
  margin-bottom: 40px;
  text-shadow: 0 0 20px rgba(52, 152, 219, 0.5);
}

.section {
  margin-bottom: 60px;
}

.section-title {
  font-size: 28px;
  font-weight: bold;
  color: #fff;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: color 0.3s;
}

.section-title:hover {
  color: #3498db;
}

.tiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
}

.tile-item {
  position: relative;
  background: rgba(20, 20, 30, 0.8);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease-in-out;
  text-align: center;
  cursor: pointer;
}

.tile-item.clickable:hover {
  transform: scale(1.05) translateY(-5px);
  box-shadow: 0 20px 40px rgba(52, 152, 219, 0.3);
}

.tile-image-container {
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

.tile-image {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tile-placeholder {
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

.tile-title {
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  margin: 15px 10px 8px;
}

.tile-years, .tile-description {
  font-size: 14px;
  color: #888;
  margin: 0 10px 15px;
}
</style>