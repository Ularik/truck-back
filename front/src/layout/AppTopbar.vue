<script setup>
import {ref, computed, onMounted, onBeforeUnmount} from 'vue';
import {useLayout} from '@/layout/composables/layout';
import {useRouter} from 'vue-router';
import Menu from 'primevue/menu';

const {changeThemeSettings, setScale, layoutConfig, onMenuToggle, isDarkTheme} = useLayout();


const outsideClickListener = ref(null);
const topbarMenuActive = ref(false);
const router = useRouter();

onMounted(() => {
  bindOutsideClickListener();
});

onBeforeUnmount(() => {
  unbindOutsideClickListener();
});

const logoUrl = computed(() => {
  return `layout/images/${layoutConfig.darkTheme.value ? 'logo-white' : 'logo-dark'}.png`;
});

const onTopBarMenuButton = () => {
  topbarMenuActive.value = !topbarMenuActive.value;
};

const topbarMenuClasses = computed(() => {
  return {
    'layout-topbar-menu-mobile-active': topbarMenuActive.value
  };
});

const bindOutsideClickListener = () => {
  if (!outsideClickListener.value) {
    outsideClickListener.value = (event) => {
      if (isOutsideClicked(event)) {
        topbarMenuActive.value = false;
      }
    };
    document.addEventListener('click', outsideClickListener.value);
  }
};
const unbindOutsideClickListener = () => {
  if (outsideClickListener.value) {
    document.removeEventListener('click', outsideClickListener);
    outsideClickListener.value = null;
  }
};
const isOutsideClicked = (event) => {
  if (!topbarMenuActive.value) return;

  const sidebarEl = document.querySelector('.layout-topbar-menu');
  const topbarEl = document.querySelector('.layout-topbar-menu-button');

  return !(sidebarEl.isSameNode(event.target) || sidebarEl.contains(event.target) || topbarEl.isSameNode(event.target) || topbarEl.contains(event.target));
};


/* Переключение в дарк режим */

const onChangeTheme = (theme, mode) => {
  const elementId = 'theme-css';
  const linkElement = document.getElementById(elementId);
  const cloneLinkElement = linkElement.cloneNode(true);
  const newThemeUrl = linkElement.getAttribute('href').replace(layoutConfig.theme.value, theme);
  cloneLinkElement.setAttribute('id', elementId + '-clone');
  cloneLinkElement.setAttribute('href', newThemeUrl);
  cloneLinkElement.addEventListener('load', () => {
    linkElement.remove();
    cloneLinkElement.setAttribute('id', elementId);
    changeThemeSettings(theme, mode === 'dark');
  });
  linkElement.parentNode.insertBefore(cloneLinkElement, linkElement.nextSibling);
};


const onDarkClick = () => {
  if (layoutConfig.darkTheme.value) {
    onChangeTheme('lara-light-indigo', 'light')
  } else {
    onChangeTheme('lara-dark-indigo', 'dark')

  }

};


const menu = ref();
const items = ref([
  {
    label: 'Профиль',
    items: [
      {
        label: 'Выход',
        icon: 'pi pi-sign-out',
        route: '/auth/login'
      },
    ]
  }
]);

const toggle = (event) => {
  menu.value.toggle(event);
};

</script>

<template>
  <div class="layout-topbar">
    <router-link to="/" class="layout-topbar-logo">
      <img :src="logoUrl" alt="logo"/>
      <span>TERMINATOR</span>
    </router-link>

    <button class="p-link layout-menu-button layout-topbar-button" @click="onMenuToggle()">
      <i class="pi pi-bars"></i>
    </button>

    <button class="p-link layout-topbar-menu-button layout-topbar-button" @click="onTopBarMenuButton()">
      <i class="pi pi-ellipsis-v"></i>
    </button>

    <div class="layout-topbar-menu" :class="topbarMenuClasses">
      <button @click="toggle" aria-haspopup="true" aria-controls="overlay_menu" class="p-link layout-topbar-button ">
        <i class="pi pi-user"></i>
        <span>Профиль</span>

      </button>
<!--      <Menu ref="menu" id="overlay_menu" :model="items" :popup="true" />-->

      <Menu ref="menu"  :model="items" :popup="true"  id="overlay_menu">
        <template #item="{ item, props }">
          <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
            <a v-ripple :href="href" v-bind="props.action" @click="navigate">
              <span :class="item.icon"/>
              <span class="ml-2">{{ item.label }}</span>
            </a>
          </router-link>
        </template>
      </Menu>


      <button @click="onDarkClick()" class="p-link layout-topbar-button">
        <i class="pi pi-moon"></i>
        <span>Settings</span>
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped></style>
