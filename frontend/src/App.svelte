<script>
  import Navbar from './components/Navbar.svelte';
  import Home from './pages/Home.svelte';
  import ChurnInputForm from './components/ChurnInputForm.svelte';

  let path = window.location.pathname;
  window.onpopstate = () => path = window.location.pathname;
</script>

<Navbar />

{#if path === "/"}
  <Home />
{:else if path === "/churn"}
  <ChurnInputForm />
{:else}
  <div class="h-screen flex items-center justify-center">
    <p class="text-xl text-red-600">404 — Page not found</p>
  </div>
{/if}
