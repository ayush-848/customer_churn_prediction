<script>
  import { BrainCog, Handshake, Users, ShieldCheck } from 'lucide-svelte';
</script>

<section class="min-h-screen bg-gray-950 text-gray-200 flex items-center justify-center py-20 px-4 sm:px-6 lg:px-8">
  <div class="max-w-4xl w-full space-y-16">

    <div class="text-center space-y-6">
      <h1 class="text-5xl md:text-6xl font-extrabold text-white leading-tight">
  ChurnPredictor
  <span class="block text-indigo-400 mt-2 text-3xl md:text-4xl font-semibold">— Stop customers before they leave</span>
</h1>
      <p class="text-lg text-gray-400 max-w-2xl mx-auto">
        Leverage advanced AI to foresee churn and deliver personalized retention strategies that increase loyalty and revenue.
      </p>
      <div class="flex justify-center">
        <a href="/churn"
           class="inline-flex items-center px-8 py-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full font-bold shadow-lg transition-all duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105">
          Predict Churn
        </a>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12">
      <div class="p-8 bg-gray-900 rounded-3xl shadow-2xl space-y-5 border border-gray-800 hover:border-indigo-600 transition-all duration-300 ease-in-out">
        <div class="flex items-center space-x-4">
          <BrainCog class="h-10 w-10 text-indigo-500 stroke-1" />
          <h3 class="text-2xl font-bold text-white">Predict Churn</h3>
        </div>
        <p class="text-gray-400 leading-relaxed">
          Upload customer data to get probability-based churn predictions and actionable strategies to reduce attrition. Understand who's at risk and why.
        </p>
      </div>

      <div class="p-8 bg-gray-900 rounded-3xl shadow-2xl space-y-5 border border-gray-800 hover:border-purple-600 transition-all duration-300 ease-in-out">
        <div class="flex items-center space-x-4">
          <Handshake class="h-10 w-10 text-purple-500 stroke-1" />
          <h3 class="text-2xl font-bold text-white">Retention Strategy</h3>
        </div>
        <p class="text-gray-400 leading-relaxed">
          Receive tailored retention suggestions based on deep behavior analytics—improve customer satisfaction and boost revenues. Keep your customers happy.
        </p>
      </div>
    </div>

    <footer class="text-center pt-16">
      <p class="text-gray-600 text-sm">
        &copy; {new Date().getFullYear()} ChurnPredictor. All rights reserved.
      </p>
    </footer>
  </div>
</section>