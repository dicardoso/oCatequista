<template>
  <div>
    <div class="app">
      
      <header class="header">
        <div class="icon">
          <img src="../assets/icon.png" width="50" srcset="">
        </div>
        <h1>O Catequista</h1>
      </header>

      <div class="input-box">
        <input
          v-model="question"
          type="text"
          placeholder="Ex: O que é o purgatório?"
          @keyup.enter="sendQuestion"
          :disabled="loading || animating"
        />
        <button :disabled="loading || animating" @click="sendQuestion">
          <span v-if="!loading && !animating">Perguntar</span>
          <div v-else class="book-flip-loader">
            <div class="page first"></div>
            <div class="page"></div>
            <div class="page"></div>
          </div>
        </button>


      </div>

      <transition name="fade">
        <div v-if="animatedAnswer" class="answer">
          <h2>{{ title }}</h2>
          <div v-html="animatedAnswer"></div>
        </div>
      </transition>
    </div>
    <a href="https://livepix.gg/dicardoso" target="_blank" class="support-button">
      Apoiar
    </a>
  </div>
</template>

<script>
import axios from 'axios'
import { marked } from 'marked'

export default {
  name: 'MainComponent',
  data() {
    return {
      question: '',
      animatedAnswer: '',
      loading: false,
      animating: false,
      title: '',
    }
  },
  methods: {
    async sendQuestion() {
      if (!this.question.trim()) return

      this.loading = true
      this.animatedAnswer = ''
      this.animating = true

      try {
        const { data } = await axios.post(
          import.meta.env.VITE_API_URL + '/question',
          { question: this.question }
        )

        const respostaHTML = marked.parse(data.answer)
        this.title = this.gerarTitulo(this.question)
        this.animarRespostaHTML(respostaHTML)
      } catch (err) {
        this.animatedAnswer = '<p><strong>Erro ao buscar resposta.</strong></p>'
        this.animating = false
      } finally {
        this.loading = false
      }
    },
    gerarTitulo(question) {
      const match = question.match(/o que (é|significa) (.+)/i)
      return match ? this.capitalizar(match[2]) : 'Resposta'
    },
    capitalizar(str) {
      return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
    },
    animarRespostaHTML(html) {
      let i = 0
      this.animatedAnswer = ''

      const escrever = () => {
        if (i < html.length) {
          this.animatedAnswer += html.charAt(i)
          i++
          setTimeout(escrever, 3)
        } else {
          this.animating = false
        }
      }

      escrever()
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..800;1,400..800&display=swap');
.app {
  width: 70%;
  min-width: 70vw;
  margin: auto;
  background-color: #fffbea;
  padding: 1.5rem;
  border-radius: 20px;
  font-family: 'Georgia', serif;
  color: #333;
  min-height: 90vh;
  box-sizing: border-box;
}

.header {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fcd34d;
  border-radius: 20px 20px 0 0;
  padding: 1rem;
  text-align: center;
  position: relative;
}

.header h1 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: bold;
}

.icon { 
  font-size: 1.5rem;
}

.input-box {
  display: flex;
  flex-direction: column;
  width: 50%;
  margin: auto;
  gap: 1rem;
  padding: 1rem 0;
}
.input-box button {
  width: 50%;
  margin: auto;
  color: #333;
}

input[type='text'] {
  padding: 0.8rem;
  font-size: 1rem;
  border-radius: 12px;
  border: 1px solid #ccc;
}

button {
  padding: 0.8rem;
  font-size: 1rem;
  background: #fcd34d;
  border: none;
  border-radius: 12px;
  font-weight: bold;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.answer {
  text-align: justify;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 16px;
  padding: 1rem;
  margin-top: 1rem;
  height: calc(100vh - 400px);
  overflow-y: auto;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  animation: fade-in 0.4s ease-in;
  
  border: 1px solid #d8cba0;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.05);
}

.answer h2 {
  margin-top: 0;
  font-size: 1.2rem;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.book-flip-loader {
  position: relative;
  top: 50%;
  left: 50%;
  width: 18px;
  height: 24px;
  perspective: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.page {
  position: absolute;
  width: 100%;
  height: 100%;
  background: #fff;
  border: 1px solid #333;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
  transform-origin: left center;
  animation: flipPage 1.2s infinite;
  border-radius: 2px;
}
.first {
  background: #fcd34d;
}

.page:nth-child(2) {
  animation-delay: 0.3s;
}
.page:nth-child(3) {
  animation-delay: 0.6s;
}

@keyframes flipPage {
  0% {
    transform: rotateY(0deg);
    opacity: 0.7;
  }
  50% {
    transform: rotateY(-120deg);
    opacity: 0.4;
  }
  100% {
    transform: rotateY(-180deg);
    opacity: 0;
  }
}

/* Responsividade */
@media (max-width: 768px) {
  .app {
    width: 90%;
    padding: 1rem;
  }

  .header h1 {
    font-size: 1.5rem;
  }

  .input-box {
    width: 100%;
  }

  .input-box button {
    width: 100%;
  }

  input[type='text'] {
    font-size: 0.9rem;
  }

  button {
    font-size: 0.9rem;
  }

  .answer {
    height: auto;
    max-height: 50vh;
  }
  
  .support-button {
    font-size: 0.5rem;
    padding: 0.4rem 0.8rem;
    top: 3.5rem;
    right: 0.8rem;
  }
}

@media (max-width: 480px) {
  .header h1 {
    font-size: 1.2rem;
  }

  .icon img {
    width: 40px;
  }

  input[type='text'] {
    font-size: 0.8rem;
    padding: 0.6rem;
  }

  button {
    font-size: 0.8rem;
    padding: 0.6rem;
  }
  .support-button {
    font-size: 0.7rem;
    padding: 0.3rem 0.6rem;
    top: 0.6rem;
    right: 0.6rem;
  }
}
.support-button {
  font-size: 0.9rem;
  font-weight: bold;
  color: #fff;
  text-decoration: none;
  background: none;
  border: 1px solid #fff;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.support-button:hover {
  background-color: #fff;
  color: #333;
}
</style>
