<script setup>
import {useLayout} from '@/layout/composables/layout';
import {ref, computed, inject} from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

localStorage.setItem(`__token`, null);

import {api, showCatch} from '@/modules/core/api'

import {useToast} from "primevue/usetoast";

const toast = useToast();

const {layoutConfig} = useLayout();
const user_name = ref('');
const password = ref('');


const logoUrl = computed(() => {
  return `layout/images/${layoutConfig.darkTheme.value ? 'logo-white' : 'logo-dark'}.png`;
});


const submitForm = async () => {
  try {
    const response = await api.post('/api/token/get', {
      user_name: user_name.value,
      password: password.value,
    });

    localStorage.setItem(`__token`, response.data.access);
    setTimeout(() => {
      api.defaults.headers.Authorization = "Bearer " + response.data.access;

      if (window.history.state.back !== null) {
        router.back();
      } else {
        router.push('/');
      }

    }, 250);

    console.log('Login successful:', response.data);
  } catch (error) {
    // showCatch(error, toast)
  }
};


</script>


<template>

  <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
    <div class="flex flex-column align-items-center justify-content-center">
      <div
          style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
        <div class="w-full surface-card py-5 px-5 sm:px-5" style="border-radius: 53px">
          <div class="text-center mb-5">
            <img :src="logoUrl" alt="Image" height="50" class="mb-3"/>
            <div class="text-900 text-3xl font-medium mb-3">I've back</div>
          </div>

          <form @submit.prevent="submitForm">
            <label for="email1" class="block text-900 text-xl font-medium mb-2">Логин</label>
            <InputText id="user_name" type="text" placeholder="Логин" class="w-full md:w-30rem mb-5"
                       style="padding: 1rem" v-model="user_name"/>

            <label for="password1" class="block text-900 font-medium text-xl mb-2">Пароль</label>
            <Password id="password1" v-model="password" placeholder="Password" :toggleMask="true" :feedback="false"
                      class="w-full mb-3" inputClass="w-full" :inputStyle="{ padding: '1rem' }"></Password>

            <Button type="submit" label="Вход" class="w-full p-3 text-xl mt-3"></Button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pi-eye {
  transform: scale(1.6);
  margin-right: 1rem;
}

.pi-eye-slash {
  transform: scale(1.6);
  margin-right: 1rem;
}
</style>
