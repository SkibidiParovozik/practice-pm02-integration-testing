<template>
  <div class="layout-container">
    <!-- Шапка -->
    <header class="header">
      <div class="header-container">
        <router-link to="/" class="logo">
          <i class="fa-solid fa-gear"></i>
          <span>Каталоги</span>
        </router-link>
        
        <div class="search-bar">
          <input 
            type="text" 
            v-model="searchQuery"
            @keyup.enter="performSearch"
            placeholder="Поиск"
            class="search-input"
          >
          <i class="fa-solid fa-search search-icon"></i>
          <button @click="performSearch" class="search-button">
            <i class="fa-solid fa-magnifying-glass"></i>
          </button>
        </div>
        
        <button class="login-button">
          <i class="fa-solid fa-right-to-bracket"></i>
          <span>Войти</span>
        </button>
      </div>
    </header>

    <!-- Основной контент -->
    <main class="main-content">
      <div class="container">
        <slot></slot>
      </div>
    </main>

    <!-- Футер -->
    <footer class="footer">
      <div class="container">
        <div class="footer-grid">
          <div class="footer-section">
            <h4>О компании</h4>
            <p>Каталог автозапчастей - ваш надежный помощник в поиске деталей для автомобиля.</p>
          </div>
          <div class="footer-section">
            <h4>Информация</h4>
            <ul>
              <li><a href="#">О нас</a></li>
              <li><a href="#">Контакты</a></li>
              <li><a href="#">Доставка</a></li>
            </ul>
          </div>
          <div class="footer-section">
            <h4>Контакты</h4>
            <p><i class="fa-solid fa-phone"></i> +7 (999) 123-45-67</p>
            <p><i class="fa-solid fa-envelope"></i> info@autospares.ru</p>
            <p class="copyright">© 2026 АвтоЗапЧасть. Все права защищены.</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const searchQuery = ref('');

const performSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/search?q=${encodeURIComponent(searchQuery.value)}`);
  }
};
</script>

<style scoped>
/* Основной контейнер */
.layout-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f3f4f6;
}

/* Шапка */
.header {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 50;
  padding: 12px 0;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

/* Логотип */
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #dc2626;
  text-decoration: none;
  font-size: 20px;
  font-weight: 700;
  transition: color 0.2s;
}

.logo:hover {
  color: #b91c1c;
}

.logo i {
  font-size: 24px;
}

/* Поиск */
.search-bar {
  flex: 1;
  max-width: 640px;
  position: relative;
  display: flex;
}

.search-input {
  width: 100%;
  background-color: #f3f4f6;
  border: none;
  border-radius: 8px 0 0 8px;
  padding: 10px 16px 10px 40px;
  font-size: 14px;
  outline: none;
  transition: box-shadow 0.2s;
}

.search-input:focus {
  box-shadow: 0 0 0 2px #dc2626;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.search-button {
  background-color: #dc2626;
  color: white;
  border: none;
  border-radius: 0 8px 8px 0;
  padding: 10px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-button:hover {
  background-color: #b91c1c;
}

/* Кнопка входа */
.login-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  color: #4b5563;
  cursor: pointer;
  font-size: 12px;
  transition: color 0.2s;
}

.login-button:hover {
  color: #dc2626;
}

.login-button i {
  font-size: 20px;
}

/* Основной контент */
.main-content {
  flex: 1;
  padding: 32px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

/* Футер */
.footer {
  background-color: #1f2937;
  color: #d1d5db;
  padding: 32px 0;
  margin-top: auto;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 32px;
}

.footer-section h4 {
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
}

.footer-section p {
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 8px;
}

.footer-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-section li {
  margin-bottom: 8px;
}

.footer-section a {
  color: #d1d5db;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s;
}

.footer-section a:hover {
  color: #ffffff;
}

.footer-section i {
  margin-right: 8px;
  width: 16px;
}

.copyright {
  margin-top: 16px;
  color: #6b7280;
  font-size: 12px;
}

/* Адаптивность */
@media (max-width: 768px) {
  .header-container {
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .search-bar {
    order: 3;
    flex-basis: 100%;
    max-width: 100%;
  }
  
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}
</style>