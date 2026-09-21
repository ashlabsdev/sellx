<script setup lang="ts">
import { ref } from 'vue'
import {
  useRouter,
} from 'vue-router'

import {
  loginAdmin,
} from '../../services/api'

import {
  setToken,
} from '../../services/auth'


const router = useRouter()

const email = ref('')
const password = ref('')

const errorMessage = ref('')
const isLoading = ref(false)


async function handleLogin() {
  errorMessage.value = ''

  if (
    !email.value.trim() ||
    !password.value
  ) {
    errorMessage.value =
      'Enter your email and password.'

    return
  }

  isLoading.value = true

  try {
    const response = await loginAdmin({
      email: email.value.trim(),
      password: password.value,
    })

    setToken(
      response.access_token,
    )

    await router.push('/admin')
  } catch (error) {
    console.error(error)

    errorMessage.value =
      'Invalid email or password.'
  } finally {
    isLoading.value = false
  }
}
</script>


<template>
  <main class="login-page">
    <section class="login-card">
      <div class="login-heading">
        <p class="eyebrow">
          SellX Admin
        </p>

        <h1>Welcome back</h1>

        <p>
          Sign in to manage your SellX
          marketplace.
        </p>
      </div>

      <form
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <label>
          <span>Email</span>

          <input
            v-model="email"
            type="email"
            autocomplete="email"
            placeholder="admin@example.com"
            :disabled="isLoading"
          />
        </label>

        <label>
          <span>Password</span>

          <input
            v-model="password"
            type="password"
            autocomplete="current-password"
            placeholder="Enter your password"
            :disabled="isLoading"
          />
        </label>

        <p
          v-if="errorMessage"
          class="error-message"
        >
          {{ errorMessage }}
        </p>

        <button
          type="submit"
          :disabled="isLoading"
        >
          {{
            isLoading
              ? 'Signing in...'
              : 'Sign in'
          }}
        </button>
      </form>

      <RouterLink
        to="/"
        class="back-link"
      >
        ← Back to marketplace
      </RouterLink>
    </section>
  </main>
</template>


<style scoped>
.login-page {
  display: grid;
  min-height: calc(100vh - 72px);
  place-items: center;
  padding: 40px 20px;
}

.login-card {
  width: 100%;
  max-width: 440px;
  padding: 36px;
  border: 1px solid #e5e5e5;
  border-radius: 18px;
  background: #fff;
  box-shadow:
    0 18px 50px
    rgba(0, 0, 0, 0.06);
}

.login-heading {
  margin-bottom: 28px;
}

.eyebrow {
  margin: 0 0 8px;
  color: #666;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.login-heading h1 {
  margin: 0 0 10px;
  font-size: 30px;
}

.login-heading p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

.login-form {
  display: grid;
  gap: 18px;
}

.login-form label {
  display: grid;
  gap: 8px;
}

.login-form label span {
  font-size: 14px;
  font-weight: 600;
}

.login-form input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #d5d5d5;
  border-radius: 10px;
  outline: none;
}

.login-form input:focus {
  border-color: #111;
}

.login-form button {
  min-height: 46px;
  border: 0;
  border-radius: 10px;
  background: #111;
  color: #fff;
  font-weight: 700;
}

.login-form button:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}

.error-message {
  margin: 0;
  color: #b42318;
  font-size: 14px;
}

.back-link {
  display: inline-block;
  margin-top: 24px;
  color: #555;
  font-size: 14px;
  text-decoration: none;
}

.back-link:hover {
  color: #111;
}
</style>