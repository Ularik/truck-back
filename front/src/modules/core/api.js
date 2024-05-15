import axios from "axios";

export const api = axios.create({
  baseURL: window.myApp.apiUrl,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer " + localStorage.getItem("__token"),
  },
});


// // Добавление перехватчика для обработки ошибок
// api.interceptors.response.use(
//   // Перехват успешного ответа
//   (response) => {
//     // Возвращаем данные, если запрос прошёл успешно
//     return response.data;
//   },
//   // Перехват ошибки
//   (error) => {
//     // Если ошибка связана с сетью
//     if (error.response) {
//       // Обработка HTTP-ошибок
//       console.log('HTTP error:', error.response.status);
//       console.log('Response data:', error.response.data);
//       console.log('Response headers:', error.response.headers);
//     } else if (error.request) {
//       // Если запрос был сделан, но сервер не ответил
//       console.log('No response received');
//     } else {
//       // Ошибка на этапе настройки запроса
//       console.log('Error in request setup:', error.message);
//     }
//     // Возвращаем ошибку для дальнейшей обработки
//     return Promise.reject(error);
//   }
// );

const TIME_MESSAGE = 5000
export const showCatch = (error, toast) => {
  switch (error.request.status) {
    case 403:
      toast.add({
        severity: 'error', life: TIME_MESSAGE,
        summary: `Доступ запрещен ${error.request.status}`,
        detail: 'Возможно нужна авторизация',
      });
      break;
    case 401:
      toast.add({
        severity: 'error', life: TIME_MESSAGE,
        summary: `Доступ запрещен ${error.request.status}`,
        detail: 'Проверьте логин и пароль!',
      });
      break;
    case 0:
      toast.add({
        severity: 'warn', life: TIME_MESSAGE,
        summary: `Нет связи с сервером ${error.request.status}`,
        detail: 'Попробуйте позднее!',
      });
      break;
    case 500:
      toast.add({
        severity: 'warn', life: TIME_MESSAGE,
        summary: `Ошибка сервера ${error.request.status}`,
        detail: 'Попробуйте позже!',
      });
      break;

    case 404:
      toast.add({
        severity: 'warn', life: TIME_MESSAGE,
        summary: `Запрос не найден ${error.request.status}`,
        detail: 'Попробуйте позже!',
      });
      break;

    case 400:
      console.log(error)
      toast.add({
        severity: 'warn', life: TIME_MESSAGE,
        summary: `Ошибка ввода данных ${error.request.status}`,
        detail: error.request.response,
      });
      break;

    default:
      toast.add({
        severity: 'error',
        life: TIME_MESSAGE,
        summary: 'Неизвестная ошибка',
        detail: error,
      });
      break;
  }

  console.error('Login error:', error);
}