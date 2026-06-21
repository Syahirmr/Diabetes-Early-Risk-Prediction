import Alpine from 'https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/module.esm.js';
import collapse from 'https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/module.esm.js';
import './services/api_client.js';
import { appStore } from './store/app_store.js';

window.Alpine = Alpine;
Alpine.plugin(collapse);
Alpine.data('appStore', appStore);
Alpine.start();
