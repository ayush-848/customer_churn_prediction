<script>
  import { BrainCog, Handshake, Users, ShieldCheck } from 'lucide-svelte';
</script>

<section class="bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-700">
  <div class="container mx-auto px-6 py-20 lg:py-32 space-y-16">

    <!-- Hero Header -->
    <div class="text-center max-w-2xl mx-auto space-y-6">
      <h1 class="text-5xl font-extrabold text-gray-900 dark:text-white leading-tight">
        ChurnPredictor — Stop customers before they leave
      </h1>
      <p class="text-lg text-gray-600 dark:text-gray-300">
        Leverage advanced AI to foresee churn and deliver personalized retention strategies that increase loyalty and revenue.
      </p>
      <div class="flex justify-center space-x-4">
        <a href="/churn"
           class="inline-flex items-center px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium shadow-lg transition">
          Predict Churn
        </a>
        <a href="/recommend"
           class="inline-flex items-center px-6 py-3 border border-indigo-600 hover:bg-indigo-100 dark:hover:bg-gray-700 text-indigo-600 dark:text-indigo-400 rounded-lg font-medium transition">
          Get Recommendation
        </a>
      </div>
    </div>

    <!-- Features Section -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="p-8 bg-white dark:bg-gray-800 rounded-xl shadow-lg space-y-4">
        <div class="flex items-center space-x-3">
          <BrainCog class="h-8 w-8 text-indigo-500" />
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Predict Churn</h3>
        </div>
        <p class="text-gray-600 dark:text-gray-300">
          Upload customer data to get probability-based churn predictions and actionable strategies to reduce attrition.
        </p>
      </div>

      <div class="p-8 bg-white dark:bg-gray-800 rounded-xl shadow-lg space-y-4">
        <div class="flex items-center space-x-3">
          <Handshake class="h-8 w-8 text-purple-500" />
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Retention Strategy</h3>
        </div>
        <p class="text-gray-600 dark:text-gray-300">
          Receive tailored retention suggestions based on behavior analytics—improve customer satisfaction and boost revenues.
        </p>
      </div>
    </div>

    <!-- Testimonials Section -->
    <div class="text-center space-y-6">
      <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Trusted by leading enterprises</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
          <p class="text-gray-600 dark:text-gray-300 italic">
            “ChurnPredictor helped us reduce churn by 20% in just two quarters. The insights are spot on.”
          </p>
          <p class="mt-4 font-semibold text-gray-900 dark:text-white">— Jane Doe, Customer Success Lead</p>
        </div>
        <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
          <p class="text-gray-600 dark:text-gray-300 italic">
            “Precision recommendations meant we re-engaged customers before they even thought of leaving.”
          </p>
          <p class="mt-4 font-semibold text-gray-900 dark:text-white">— Raj Patel, Head of Marketing</p>
        </div>
        <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
          <p class="text-gray-600 dark:text-gray-300 italic">
            “Seamless integration and immediate ROI. A must-have for SaaS companies.”
          </p>
          <p class="mt-4 font-semibold text-gray-900 dark:text-white">— Li Wei, CTO</p>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="text-center py-8">
      <p class="text-gray-600 dark:text-gray-400">
        &copy; {new Date().getFullYear()} ChurnPredictor. All rights reserved.
      </p>
    </footer>
  </div>
</section>
