<script>
    import { writable } from 'svelte/store';
    import { onMount } from 'svelte';

    const URL=import.meta.env.VITE_API_URL;
    const API_URL = `${URL}/predict_churn/`;

    // Form data store
    const formDataStore = writable({
        Age: null,
        Gender: '',
        Tenure: null,
        Usage_Frequency: null,
        Support_Calls: null,
        Payment_Delay: null,
        Subscription_Type: '',
        Contract_Length: '',
        Last_Interaction: null
    });

    let result = null;
    let error = null;
    let loading = false;

    let formData = { ...$formDataStore };

    async function handleSubmit() {
        loading = true;
        result = null;
        error = null;

        const payload = {};
        for (const key in formData) {
            if (formData.hasOwnProperty(key)) {
                if (['Age', 'Tenure', 'Usage_Frequency', 'Support_Calls', 'Payment_Delay', 'Last_Interaction'].includes(key)) {
                    payload[key] = formData[key] !== null && formData[key] !== '' ? parseFloat(formData[key]) : null;
                } else {
                    payload[key] = formData[key];
                }
            }
        }
        
        for (const key in payload) {
            if (payload[key] === '' || payload[key] === undefined || payload[key] === null) {
                error = `Please fill in all fields. Missing: ${key.replace(/_/g, ' ')}`;
                loading = false;
                return;
            }
        }

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail ? JSON.stringify(errorData.detail) : 'Failed to fetch prediction from API. Check server logs.');
            }

            result = await response.json();

        } catch (err) {
            console.error("API request failed:", err);
            error = `Connection Error: ${err.message}. Make sure your FastAPI backend is running and reachable!`;
        } finally {
            loading = false;
        }
    }

    function resetForm() {
        formData = {
            Age: null,
            Gender: '',
            Tenure: null,
            Usage_Frequency: null,
            Support_Calls: null,
            Payment_Delay: null,
            Subscription_Type: '',
            Contract_Length: '',
            Last_Interaction: null
        };
        result = null;
        error = null;
    }
</script>

<div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <div class="max-w-6xl mx-auto px-6 py-8">
        
        <!-- Header Section -->
        <div class="text-center mb-10">
            <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-slate-700 to-slate-900 rounded-2xl mb-6">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
            </div>
            <h1 class="text-4xl font-bold text-gray-900 mb-3">
                Customer Churn Predictor
            </h1>
            <p class="text-xl text-gray-600 max-w-2xl mx-auto">
                Leverage AI-powered analytics to predict customer retention and optimize your business strategy
            </p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <!-- Form Section -->
            <div class="lg:col-span-2">
                <div class="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
                    <div class="bg-gradient-to-r from-slate-700 to-slate-900 px-8 py-6">
                        <h2 class="text-2xl font-semibold text-white">Customer Information</h2>
                        <p class="text-slate-200 mt-1">Enter customer details for churn prediction</p>
                    </div>
                    
                    <div class="p-8">
                        <form on:submit|preventDefault={handleSubmit} class="space-y-8">
                            
                            <!-- Personal Information -->
                            <div class="space-y-6">
                                <h3 class="text-lg font-semibold text-gray-900 border-b border-gray-200 pb-2">
                                    Personal Details
                                </h3>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div class="space-y-2">
                                        <label for="age" class="block text-sm font-semibold text-gray-700">Age</label>
                                        <input 
                                            type="number" 
                                            id="age" 
                                            placeholder="e.g., 35" 
                                            bind:value={formData.Age} 
                                            required 
                                            min="0" 
                                            max="100"
                                            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-600 focus:border-transparent bg-gray-50 text-gray-900 placeholder-gray-500 transition-all duration-200"
                                        />
                                    </div>

                                    <div class="space-y-2">
                                        <label for="gender" class="block text-sm font-semibold text-gray-700">Gender</label>
                                        <select 
                                            id="gender" 
                                            bind:value={formData.Gender} 
                                            required
                                            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-600 focus:border-transparent bg-gray-50 text-gray-900 transition-all duration-200"
                                        >
                                            <option value="" disabled>Select Gender</option>
                                            <option value="Male">Male</option>
                                            <option value="Female">Female</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <!-- Service Information -->
                            <div class="space-y-6">
                                <h3 class="text-lg font-semibold text-gray-900 border-b border-gray-200 pb-2">
                                    Service Details
                                </h3>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div class="space-y-2">
                                        <label for="tenure" class="block text-sm font-semibold text-gray-700">Tenure (in months)</label>
                                        <div class="relative">
                                            <input 
                                                type="number" 
                                                id="tenure" 
                                                placeholder="24" 
                                                bind:value={formData.Tenure} 
                                                required 
                                                min="0"
                                                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-600 focus:border-transparent bg-gray-50 text-gray-900 placeholder-gray-500 transition-all duration-200"
                                            />
                                        </div>
                                    </div>

                                    <div class="space-y-2">
                                        <label for="usageFrequency" class="block text-sm font-semibold text-gray-700">Usage Frequency (Per month)</label>
                                        <div class="relative">
                                            <input 
                                                type="number" 
                                                id="usageFrequency" 
                                                placeholder="10" 
                                                bind:value={formData.Usage_Frequency} 
                                                required 
                                                min="0"
                                                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-600 focus:border-transparent bg-gray-50 text-gray-900 placeholder-gray-500 transition-all duration-200"
                                            />
                                         </div>
                                    </div>

                                    <div class="space-y-2">
                                        <label for="supportCalls" class="block text-sm font-semibold text-gray-700">Support Calls (in months)</label>
                                        <div class="relative">
                                            <input 
                                                type="number" 
                                                id="supportCalls" 
                                                placeholder="2" 
                                                bind:value={formData.Support_Calls} 
                                                required 
                                                min="0"
                                                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-600 focus:border-transparent bg-gray-50 text-gray-900 placeholder-gray-500 transition-all duration-200"
                                            />
                                        </div>
                                    </div>

                                    <div class="space-y-2">
                                        <label for="paymentDelay" class="block text-sm font-semibold text-gray-700">Payment Delay (in days)</label>
                                        <div class="relative">
                                            <input 
                                                type="number" 
                                                id="paymentDelay" 
                                                placeholder="5" 
                                                bind:value={formData.Payment_Delay} 
                                                required 
                                                min="0"
                                                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-600 focus:border-transparent bg-gray-50 text-gray-900 placeholder-gray-500 transition-all duration-200"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Subscription Information -->
                            <div class="space-y-6">
                                <h3 class="text-lg font-semibold text-gray-900 border-b border-gray-200 pb-2">
                                    Subscription Details
                                </h3>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div class="space-y-2">
                                        <label for="subscriptionType" class="block text-sm font-semibold text-gray-700">Subscription Type</label>
                                        <select 
                                            id="subscriptionType" 
                                            bind:value={formData.Subscription_Type} 
                                            required
                                            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-600 focus:border-transparent bg-gray-50 text-gray-900 transition-all duration-200"
                                        >
                                            <option value="" disabled>Select Type</option>
                                            <option value="Basic">Basic</option>
                                            <option value="Standard">Standard</option>
                                            <option value="Premium">Premium</option>
                                        </select>
                                    </div>

                                    <div class="space-y-2">
                                        <label for="contractLength" class="block text-sm font-semibold text-gray-700">Contract Length</label>
                                        <select 
                                            id="contractLength" 
                                            bind:value={formData.Contract_Length} 
                                            required
                                            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-600 focus:border-transparent bg-gray-50 text-gray-900 transition-all duration-200"
                                        >
                                            <option value="" disabled>Select Length</option>
                                            <option value="Monthly">Monthly</option>
                                            <option value="Quarterly">Quarterly</option>
                                            <option value="Annual">Annual</option>
                                        </select>
                                    </div>

                                    <div class="space-y-2 md:col-span-2">
                                        <label for="lastInteraction" class="block text-sm font-semibold text-gray-700">Last Interaction (in days)</label>
                                        <div class="relative">
                                            <input 
                                                type="number" 
                                                id="lastInteraction" 
                                                placeholder="7" 
                                                bind:value={formData.Last_Interaction} 
                                                required 
                                                min="0"
                                                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-600 focus:border-transparent bg-gray-50 text-gray-900 placeholder-gray-500 transition-all duration-200"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Action Buttons -->
                            <div class="flex gap-4 pt-6 border-t border-gray-200">
                                <button 
                                    type="submit" 
                                    disabled={loading}
                                    class="flex-1 py-4 px-6 bg-gradient-to-r from-slate-700 to-slate-900 text-white font-semibold rounded-xl hover:from-slate-800 hover:to-slate-950 focus:outline-none focus:ring-2 focus:ring-slate-600 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg"
                                >
                                    {#if loading}
                                        <div class="flex items-center justify-center">
                                            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                            </svg>
                                            Analyzing...
                                        </div>
                                    {:else}
                                        Predict Churn Risk
                                    {/if}
                                </button>
                                <button 
                                    type="button" 
                                    on:click={resetForm} 
                                    class="px-6 py-4 border-2 border-gray-300 text-gray-700 font-semibold rounded-xl hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-slate-600 focus:ring-offset-2 transition-all duration-200"
                                >
                                    Reset Form
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Results Section -->
            <div class="lg:col-span-1">
                <div class="sticky top-8 space-y-6">
                    
                    <!-- Error Message -->
                    {#if error}
                        <div class="bg-red-50 border-l-4 border-red-400 rounded-xl p-6 shadow-lg">
                            <div class="flex items-center">
                                <svg class="w-6 h-6 text-red-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                                </svg>
                                <div>
                                    <h3 class="text-red-800 font-semibold">Error</h3>
                                    <p class="text-red-700 text-sm mt-1">{error}</p>
                                </div>
                            </div>
                        </div>
                    {/if}

                    <!-- Results Card -->
                    {#if result}
                        <div class="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
                            <div class="bg-gradient-to-r {result.predicted_churn === 1 ? 'from-red-500 to-red-600' : 'from-green-500 to-green-600'} px-6 py-4">
                                <div class="flex items-center">
                                    <div class="w-10 h-10 bg-white bg-opacity-20 rounded-full flex items-center justify-center mr-3">
                                        {#if result.predicted_churn === 1}
                                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                                            </svg>
                                        {:else}
                                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                            </svg>
                                        {/if}
                                    </div>
                                    <div>
                                        <h2 class="text-xl font-bold text-white">
                                            {result.predicted_churn === 1 ? 'High Risk' : 'Low Risk'}
                                        </h2>
                                        <p class="text-white text-opacity-90 text-sm">
                                            {result.predicted_churn === 1 ? 'Customer likely to churn' : 'Customer likely to stay'}
                                        </p>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="p-6 space-y-6">
                                <!-- Key Metrics -->
                                <div class="space-y-4">
                                    <div class="flex justify-between items-center py-3 border-b border-gray-100">
                                        <span class="text-gray-600 font-medium">Churn Probability</span>
                                        <div class="text-right">
                                            <span class="text-2xl font-bold text-gray-900">
                                                {(result.churn_probability * 100).toFixed(1)}%
                                            </span>
                                        </div>
                                    </div>
                                    
                                    <div class="flex justify-between items-center py-3 border-b border-gray-100">
                                        <span class="text-gray-600 font-medium">Risk Level</span>
                                        <span class="font-semibold px-3 py-1 rounded-full text-sm
                                            {result.churn_risk_level === 'High' ? 'bg-red-100 text-red-700' : 
                                              result.churn_risk_level === 'Medium' ? 'bg-yellow-100 text-yellow-700' : 
                                              'bg-green-100 text-green-700'}">
                                            {result.churn_risk_level}
                                        </span>
                                    </div>
                                </div>
                                
                                <!-- Strategy Section -->
                                <div class="space-y-4">
                                    <div class="bg-gray-50 rounded-xl p-4">
                                        <h3 class="font-semibold text-gray-900 mb-2 flex items-center">
                                            <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 017.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                                            </svg>
                                            Recommended Strategy
                                        </h3>
                                        <p class="text-gray-700 text-sm leading-relaxed">{result.retention_strategy}</p>
                                    </div>
                                    
                                    <div class="bg-blue-50 rounded-xl p-4">
                                        <h3 class="font-semibold text-blue-900 mb-2 flex items-center">
                                            <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                            </svg>
                                            Insights
                                        </h3>
                                        <p class="text-blue-800 text-sm leading-relaxed">{result.message}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {/if}

                    <!-- Info Card -->
                    {#if !result && !error}
                        <div class="bg-white rounded-2xl shadow-xl border border-gray-200 p-6">
                            <div class="text-center">
                                <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                </div>
                                <h3 class="text-lg font-semibold text-gray-900 mb-2">Ready to Analyze</h3>
                                <p class="text-gray-600 text-sm">Fill in the customer information and click "Predict Churn Risk" to get AI-powered insights.</p>
                            </div>
                        </div>
                    {/if}
                </div>
            </div>
        </div>
    </div>
</div>