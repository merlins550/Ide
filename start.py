<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexusFlow - LLM Chain Automation Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .animate-pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
        .gradient-bg {
            background: linear-gradient(135deg, #6e8efb 0%, #a777e3 100%);
        }
        .chain-node {
            position: relative;
        }
        .chain-node:not(:last-child):after {
            content: "";
            position: absolute;
            right: -20px;
            top: 50%;
            width: 20px;
            height: 2px;
            background: #a0aec0;
        }
        .scrollbar-hide::-webkit-scrollbar {
            display: none;
        }
        .scrollbar-hide {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        .prompt-editor {
            min-height: 120px;
            border: 1px solid #e2e8f0;
            border-radius: 0.375rem;
            padding: 0.75rem;
        }
        .prompt-editor:focus {
            outline: none;
            border-color: #a777e3;
            box-shadow: 0 0 0 1px #a777e3;
        }
        .ollama-badge {
            background-color: #3B82F6;
            color: white;
        }
    </style>
</head>
<body class="bg-gray-50 h-screen flex overflow-hidden">
    <!-- Sidebar -->
    <div class="w-16 bg-white shadow-md flex flex-col items-center py-4">
        <div class="gradient-bg rounded-lg p-2 mb-6">
            <i class="fas fa-link text-white text-xl"></i>
        </div>
        <button id="chat-btn" class="w-12 h-12 rounded-lg mb-3 flex items-center justify-center bg-indigo-100 text-indigo-600">
            <i class="fas fa-comment-dots text-xl"></i>
        </button>
        <button id="chain-btn" class="w-12 h-12 rounded-lg mb-3 flex items-center justify-center hover:bg-gray-100 text-gray-600">
            <i class="fas fa-link text-xl"></i>
        </button>
        <button id="history-btn" class="w-12 h-12 rounded-lg mb-3 flex items-center justify-center hover:bg-gray-100 text-gray-600">
            <i class="fas fa-history text-xl"></i>
        </button>
        <div class="mt-auto">
            <button id="settings-btn" class="w-12 h-12 rounded-lg flex items-center justify-center hover:bg-gray-100 text-gray-600">
                <i class="fas fa-cog text-xl"></i>
            </button>
        </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Header -->
        <header class="bg-white shadow-sm py-3 px-6 flex items-center justify-between">
            <h1 class="text-xl font-semibold text-gray-800">NexusFlow</h1>
            <div class="flex items-center space-x-4">
                <div class="relative">
                    <button class="flex items-center space-x-2 bg-gray-100 hover:bg-gray-200 rounded-full px-4 py-1.5">
                        <span class="text-sm font-medium text-gray-700">New Session</span>
                        <i class="fas fa-plus text-gray-500"></i>
                    </button>
                </div>
                <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center">
                    <i class="fas fa-user text-indigo-600"></i>
                </div>
            </div>
        </header>

        <!-- Dynamic Content Area -->
        <div class="flex-1 overflow-hidden flex">
            <!-- Chat Interface (Default View) -->
            <div id="chat-view" class="flex-1 flex flex-col h-full">
                <!-- Chat Messages -->
                <div class="flex-1 overflow-y-auto p-6 space-y-4 scrollbar-hide">
                    <div class="flex justify-start">
                        <div class="max-w-3xl bg-white rounded-xl shadow-sm p-4">
                            <div class="flex items-center mb-2">
                                <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center mr-3">
                                    <i class="fas fa-robot text-indigo-600"></i>
                                </div>
                                <span class="font-medium text-gray-700">NexusFlow</span>
                            </div>
                            <p class="text-gray-700">Welcome to NexusFlow! I'm your LLM chain automation assistant. Start by entering your idea or question below, and I'll guide it through our optimized LLM processing pipeline.</p>
                        </div>
                    </div>
                    
                    <div class="flex justify-end">
                        <div class="max-w-3xl bg-indigo-50 rounded-xl shadow-sm p-4">
                            <div class="flex items-center mb-2">
                                <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center mr-3">
                                    <i class="fas fa-lightbulb text-indigo-600"></i>
                                </div>
                                <span class="font-medium text-gray-700">Initial Idea</span>
                            </div>
                            <p class="text-gray-700">I want to create an automated system that takes a basic product idea and develops it into a complete business plan using a chain of specialized LLMs.</p>
                        </div>
                    </div>
                    
                    <div class="flex justify-start">
                        <div class="max-w-3xl bg-white rounded-xl shadow-sm p-4">
                            <div class="flex items-center mb-2">
                                <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center mr-3">
                                    <i class="fas fa-robot text-indigo-600"></i>
                                </div>
                                <span class="font-medium text-gray-700">NexusFlow</span>
                            </div>
                            <p class="text-gray-700">Excellent! I'll process this through our 5-stage LLM chain:</p>
                            <div class="mt-3 flex space-x-2 overflow-x-auto pb-2">
                                <div class="chain-node flex flex-col items-center bg-indigo-50 rounded-lg p-3 min-w-[120px]">
                                    <div class="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center mb-2">
                                        <span class="text-indigo-600 font-bold">1</span>
                                    </div>
                                    <span class="text-xs font-medium text-gray-700">Concept Expansion</span>
                                </div>
                                <div class="chain-node flex flex-col items-center bg-indigo-50 rounded-lg p-3 min-w-[120px]">
                                    <div class="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center mb-2">
                                        <span class="text-indigo-600 font-bold">2</span>
                                    </div>
                                    <span class="text-xs font-medium text-gray-700">Market Analysis</span>
                                </div>
                                <div class="chain-node flex flex-col items-center bg-indigo-50 rounded-lg p-3 min-w-[120px]">
                                    <div class="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center mb-2">
                                        <span class="text-indigo-600 font-bold">3</span>
                                    </div>
                                    <span class="text-xs font-medium text-gray-700">Technical Feasibility</span>
                                </div>
                                <div class="chain-node flex flex-col items-center bg-indigo-50 rounded-lg p-3 min-w-[120px]">
                                    <div class="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center mb-2">
                                        <span class="text-indigo-600 font-bold">4</span>
                                    </div>
                                    <span class="text-xs font-medium text-gray-700">Business Model</span>
                                </div>
                                <div class="chain-node flex flex-col items-center bg-indigo-50 rounded-lg p-3 min-w-[120px]">
                                    <div class="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center mb-2">
                                        <span class="text-indigo-600 font-bold">5</span>
                                    </div>
                                    <span class="text-xs font-medium text-gray-700">Final Proposal</span>
                                </div>
                            </div>
                            <div class="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
                                <div class="flex items-center text-blue-600 mb-1">
                                    <i class="fas fa-info-circle mr-2"></i>
                                    <span class="text-sm font-medium">Processing Stage 1/5</span>
                                </div>
                                <p class="text-sm text-blue-800">Expanding your initial concept with market research and potential applications...</p>
                                <div class="mt-2 w-full bg-blue-100 rounded-full h-1.5">
                                    <div class="bg-blue-600 h-1.5 rounded-full animate-pulse" style="width: 20%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Input Area -->
                <div class="border-t border-gray-200 p-4">
                    <div class="max-w-4xl mx-auto">
                        <div class="flex items-end space-x-2">
                            <div class="flex-1 bg-white rounded-lg shadow-sm border border-gray-200">
                                <div class="prompt-editor" contenteditable="true" placeholder="Enter your idea or question..."></div>
                                <div class="flex justify-between items-center px-3 py-2 border-t border-gray-100">
                                    <div class="flex space-x-2">
                                        <button class="w-8 h-8 rounded hover:bg-gray-100 flex items-center justify-center text-gray-500">
                                            <i class="fas fa-paperclip"></i>
                                        </button>
                                        <button class="w-8 h-8 rounded hover:bg-gray-100 flex items-center justify-center text-gray-500">
                                            <i class="fas fa-magic"></i>
                                        </button>
                                    </div>
                                    <button class="text-sm text-gray-500 hover:text-gray-700">
                                        <i class="fas fa-sliders-h mr-1"></i> Advanced
                                    </button>
                                </div>
                            </div>
                            <button class="w-12 h-12 rounded-lg gradient-bg text-white flex items-center justify-center shadow-md hover:shadow-lg transition-shadow">
                                <i class="fas fa-paper-plane text-xl"></i>
                            </button>
                        </div>
                        <p class="text-xs text-gray-500 mt-2 px-1">NexusFlow will process your input through the configured LLM chain. <a href="#" class="text-indigo-600 hover:underline">Edit chain configuration</a></p>
                    </div>
                </div>
            </div>

            <!-- Settings View (Hidden by default) -->
            <div id="settings-view" class="hidden flex-1 flex flex-col h-full bg-white">
                <div class="border-b border-gray-200 px-6 py-4">
                    <h2 class="text-lg font-semibold text-gray-800">Settings & Configuration</h2>
                    <p class="text-sm text-gray-500">Manage your API keys and LLM chain settings</p>
                </div>
                
                <div class="flex-1 overflow-y-auto p-6">
                    <div class="max-w-4xl mx-auto space-y-8">
                        <!-- API Keys Section -->
                        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                            <div class="border-b border-gray-200 px-5 py-4 bg-gray-50">
                                <h3 class="font-medium text-gray-800">LLM Provider API Keys</h3>
                                <p class="text-sm text-gray-500 mt-1">Configure access to different LLM providers in your chain</p>
                            </div>
                            <div class="divide-y divide-gray-200">
                                <!-- OpenAI -->
                                <div class="p-5">
                                    <div class="flex items-center justify-between mb-3">
                                        <div class="flex items-center">
                                            <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center mr-3">
                                                <i class="fab fa-openai text-gray-700"></i>
                                            </div>
                                            <div>
                                                <h4 class="font-medium text-gray-800">OpenAI</h4>
                                                <p class="text-xs text-gray-500">GPT-4, GPT-3.5 models</p>
                                            </div>
                                        </div>
                                        <div class="flex items-center space-x-2">
                                            <span class="text-xs px-2 py-1 rounded bg-green-100 text-green-800">Active</span>
                                            <button class="text-gray-400 hover:text-gray-600">
                                                <i class="fas fa-ellipsis-v"></i>
                                            </button>
                                        </div>
                                    </div>
                                    <div class="pl-13">
                                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <label class="block text-sm font-medium text-gray-700 mb-1">API Key</label>
                                                <div class="relative">
                                                    <input type="password" value="sk-********************" class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 pr-10">
                                                    <button class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600">
                                                        <i class="far fa-eye"></i>
                                                    </button>
                                                </div>
                                            </div>
                                            <div>
                                                <label class="block text-sm font-medium text-gray-700 mb-1">Organization</label>
                                                <input type="text" value="org-****************" class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                                            </div>
                                        </div>
                                        <div class="mt-3 flex items-center justify-between">
                                            <div class="flex items-center space-x-2">
                                                <div class="w-2 h-2 rounded-full bg-green-500"></div>
                                                <span class="text-xs text-gray-500">Last used: 5 min ago</span>
                                            </div>
                                            <button class="text-sm text-indigo-600 hover:text-indigo-800">Test Connection</button>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Anthropic -->
                                <div class="p-5">
                                    <div class="flex items-center justify-between mb-3">
                                        <div class="flex items-center">
                                            <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center mr-3">
                                                <i class="fas fa-robot text-gray-700"></i>
                                            </div>
                                            <div>
                                                <h4 class="font-medium text-gray-800">Anthropic</h4>
                                                <p class="text-xs text-gray-500">Claude models</p>
                                            </div>
                                        </div>
                                        <div class="flex items-center space-x-2">
                                            <span class="text-xs px-2 py-1 rounded bg-yellow-100 text-yellow-800">Not Configured</span>
                                            <button class="text-gray-400 hover:text-gray-600">
                                                <i class="fas fa-ellipsis-v"></i>
                                            </button>
                                        </div>
                                    </div>
                                    <div class="pl-13">
                                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <label class="block text-sm font-medium text-gray-700 mb-1">API Key</label>
                                                <div class="relative">
                                                    <input type="password" placeholder="Enter your API key" class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 pr-10">
                                                    <button class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600">
                                                        <i class="far fa-eye"></i>
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="mt-3 flex items-center justify-end">
                                            <button class="text-sm text-indigo-600 hover:text-indigo-800">Test Connection</button>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Ollama -->
                                <div class="p-5">
                                    <div class="flex items-center justify-between mb-3">
                                        <div class="flex items-center">
                                            <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center mr-3">
                                                <i class="fas fa-server text-gray-700"></i>
                                            </div>
                                            <div>
                                                <h4 class="font-medium text-gray-800">Ollama</h4>
                                                <p class="text-xs text-gray-500">Local LLM models</p>
                                            </div>
                                        </div>
                                        <div class="flex items-center space-x-2">
                                            <span class="text-xs px-2 py-1 rounded bg-blue-100 text-blue-800 ollama-badge">Self-Hosted</span>
                                            <button class="text-gray-400 hover:text-gray-600">
                                                <i class="fas fa-ellipsis-v"></i>
                                            </button>
                                        </div>
                                    </div>
                                    <div class="pl-13">
                                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <label class="block text-sm font-medium text-gray-700 mb-1">Base URL</label>
                                                <input type="text" value="http://localhost:11434" class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                                            </div>
                                            <div>
                                                <label class="block text-sm font-medium text-gray-700 mb-1">Model</label>
                                                <select class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                                                    <option>llama3</option>
                                                    <option>mistral</option>
                                                    <option>gemma</option>
                                                    <option>phi3</option>
                                                    <option selected>Custom Model</option>
                                                </select>
                                            </div>
                                        </div>
                                        <div class="mt-4">
                                            <label class="block text-sm font-medium text-gray-700 mb-1">Custom Model Name</label>
                                            <input type="text" placeholder="my-custom-model" class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                                        </div>
                                        <div class="mt-3 flex items-center justify-between">
                                            <div class="flex items-center space-x-2">
                                                <div class="w-2 h-2 rounded-full bg-green-500"></div>
                                                <span class="text-xs text-gray-500">Connected to local Ollama instance</span>
                                            </div>
                                            <button class="text-sm text-indigo-600 hover:text-indigo-800">Test Connection</button>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Add New Provider -->
                                <div class="p-5">
                                    <button class="w-full flex items-center justify-center space-x-2 text-indigo-600 hover:text-indigo-800 py-2 rounded-md border-2 border-dashed border-gray-300 hover:border-indigo-300">
                                        <i class="fas fa-plus"></i>
                                        <span>Add LLM Provider</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Chain Configuration -->
                        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                            <div class="border-b border-gray-200 px-5 py-4 bg-gray-50">
                                <h3 class="font-medium text-gray-800">LLM Chain Configuration</h3>
                                <p class="text-sm text-gray-500 mt-1">Define the sequence and parameters for your LLM processing chain</p>
                            </div>
                            <div class="p-5">
                                <div class="space-y-6">
                                    <!-- Chain Stages -->
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-2">Chain Stages</label>
                                        <div class="space-y-3">
                                            <!-- Stage 1 -->
                                            <div class="flex items-start space-x-3 p-3 bg-indigo-50 rounded-lg">
                                                <div class="flex-shrink-0 mt-1">
                                                    <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center">
                                                        <span class="text-indigo-600 font-bold">1</span>
                                                    </div>
                                                </div>
                                                <div class="flex-1 min-w-0">
                                                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                                        <div>
                                                            <label class="block text-xs font-medium text-gray-500 mb-1">LLM Provider</label>
                                                            <select class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                                <option>OpenAI GPT-4</option>
                                                                <option>OpenAI GPT-3.5</option>
                                                                <option>Anthropic Claude 3</option>
                                                                <option selected>Ollama Llama3</option>
                                                            </select>
                                                        </div>
                                                        <div>
                                                            <label class="block text-xs font-medium text-gray-500 mb-1">Temperature</label>
                                                            <input type="range" min="0" max="1" step="0.1" value="0.7" class="w-full">
                                                            <div class="flex justify-between text-xs text-gray-500 mt-1">
                                                                <span>Precise</span>
                                                                <span>Creative</span>
                                                            </div>
                                                        </div>
                                                        <div>
                                                            <label class="block text-xs font-medium text-gray-500 mb-1">Max Tokens</label>
                                                            <input type="number" value="1000" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                        </div>
                                                    </div>
                                                    <div class="mt-3">
                                                        <label class="block text-xs font-medium text-gray-500 mb-1">Custom Prompt Template</label>
                                                        <textarea rows="2" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">Expand the following concept with detailed explanations and potential applications: {input}</textarea>
                                                    </div>
                                                </div>
                                                <button class="text-gray-400 hover:text-gray-600">
                                                    <i class="fas fa-times"></i>
                                                </button>
                                            </div>
                                            
                                            <!-- Stage 2 -->
                                            <div class="flex items-start space-x-3 p-3 bg-indigo-50 rounded-lg">
                                                <div class="flex-shrink-0 mt-1">
                                                    <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center">
                                                        <span class="text-indigo-600 font-bold">2</span>
                                                    </div>
                                                </div>
                                                <div class="flex-1 min-w-0">
                                                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                                        <div>
                                                            <label class="block text-xs font-medium text-gray-500 mb-1">LLM Provider</label>
                                                            <select class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                                <option>OpenAI GPT-4</option>
                                                                <option selected>Anthropic Claude 3</option>
                                                                <option>OpenAI GPT-3.5</option>
                                                                <option>Ollama Mistral</option>
                                                            </select>
                                                        </div>
                                                        <div>
                                                            <label class="block text-xs font-medium text-gray-500 mb-1">Temperature</label>
                                                            <input type="range" min="0" max="1" step="0.1" value="0.5" class="w-full">
                                                            <div class="flex justify-between text-xs text-gray-500 mt-1">
                                                                <span>Precise</span>
                                                                <span>Creative</span>
                                                            </div>
                                                        </div>
                                                        <div>
                                                            <label class="block text-xs font-medium text-gray-500 mb-1">Max Tokens</label>
                                                            <input type="number" value="1200" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                        </div>
                                                    </div>
                                                    <div class="mt-3">
                                                        <label class="block text-xs font-medium text-gray-500 mb-1">Custom Prompt Template</label>
                                                        <textarea rows="2" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">Analyze the following concept for market potential and competitive landscape: {input}</textarea>
                                                    </div>
                                                </div>
                                                <button class="text-gray-400 hover:text-gray-600">
                                                    <i class="fas fa-times"></i>
                                                </button>
                                            </div>
                                        </div>
                                        <button class="mt-3 flex items-center text-sm text-indigo-600 hover:text-indigo-800">
                                            <i class="fas fa-plus mr-1"></i>
                                            <span>Add Stage</span>
                                        </button>
                                    </div>
                                    
                                    <!-- Context Management -->
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-2">Context Management</label>
                                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <label class="block text-xs font-medium text-gray-500 mb-1">Context Preservation</label>
                                                <select class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                    <option>Full Context (High Cost)</option>
                                                    <option selected>Summarized Context (Recommended)</option>
                                                    <option>Minimal Context</option>
                                                </select>
                                            </div>
                                            <div>
                                                <label class="block text-xs font-medium text-gray-500 mb-1">Summary Length</label>
                                                <input type="number" value="300" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                <p class="text-xs text-gray-500 mt-1">Tokens to preserve between stages</p>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <!-- Fallback Strategy -->
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-2">Fallback Strategy</label>
                                        <div class="space-y-2">
                                            <div class="flex items-center">
                                                <input id="fallback-enabled" type="checkbox" checked class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
                                                <label for="fallback-enabled" class="ml-2 block text-sm text-gray-700">Enable automatic fallback to alternative models</label>
                                            </div>
                                            <div class="pl-6">
                                                <div class="flex items-center">
                                                    <input id="retry-enabled" type="checkbox" checked class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
                                                    <label for="retry-enabled" class="ml-2 block text-sm text-gray-700">Retry failed stages (max attempts)</label>
                                                    <input type="number" value="3" class="ml-2 w-16 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                </div>
                                                <div class="mt-2 flex items-center">
                                                    <input id="ollama-fallback" type="checkbox" checked class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
                                                    <label for="ollama-fallback" class="ml-2 block text-sm text-gray-700">Use Ollama as fallback when cloud models fail</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Save Settings -->
                        <div class="flex justify-end space-x-3">
                            <button class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                                Reset
                            </button>
                            <button class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                                Save Changes
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Toggle between chat and settings view
        document.getElementById('chat-btn').addEventListener('click', function() {
            document.getElementById('chat-view').classList.remove('hidden');
            document.getElementById('settings-view').classList.add('hidden');
            document.getElementById('chat-btn').classList.add('bg-indigo-100', 'text-indigo-600');
            document.getElementById('chat-btn').classList.remove('hover:bg-gray-100', 'text-gray-600');
            document.getElementById('settings-btn').classList.remove('bg-indigo-100', 'text-indigo-600');
            document.getElementById('settings-btn').classList.add('hover:bg-gray-100', 'text-gray-600');
        });

        document.getElementById('settings-btn').addEventListener('click', function() {
            document.getElementById('chat-view').classList.add('hidden');
            document.getElementById('settings-view').classList.remove('hidden');
            document.getElementById('settings-btn').classList.add('bg-indigo-100', 'text-indigo-600');
            document.getElementById('settings-btn').classList.remove('hover:bg-gray-100', 'text-gray-600');
            document.getElementById('chat-btn').classList.remove('bg-indigo-100', 'text-indigo-600');
            document.getElementById('chat-btn').classList.add('hover:bg-gray-100', 'text-gray-600');
        });

        // Simulate chat functionality
        document.querySelector('.fa-paper-plane').addEventListener('click', function() {
            const promptEditor = document.querySelector('.prompt-editor');
            const message = promptEditor.textContent.trim();
            
            if (message) {
                // Add user message to chat
                const chatContainer = document.querySelector('#chat-view > div.flex-1');
                const userMessageDiv = document.createElement('div');
                userMessageDiv.className = 'flex justify-end';
                userMessageDiv.innerHTML = `
                    <div class="max-w-3xl bg-indigo-50 rounded-xl shadow-sm p-4">
                        <div class="flex items-center mb-2">
                            <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center mr-3">
                                <i class="fas fa-lightbulb text-indigo-600"></i>
                            </div>
                            <span class="font-medium text-gray-700">You</span>
                        </div>
                        <p class="text-gray-700">${message}</p>
                    </div>
                `;
                chatContainer.appendChild(userMessageDiv);
                
                // Clear input
                promptEditor.textContent = '';
                
                // Add processing indicator
                const processingDiv = document.createElement('div');
                processingDiv.className = 'flex justify-start';
                processingDiv.innerHTML = `
                    <div class="max-w-3xl bg-white rounded-xl shadow-sm p-4">
                        <div class="flex items-center mb-2">
                            <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center mr-3">
                                <i class="fas fa-robot text-indigo-600"></i>
                            </div>
                            <span class="font-medium text-gray-700">NexusFlow</span>
                        </div>
                        <div class="p-3 bg-blue-50 rounded-lg border border-blue-100">
                            <div class="flex items-center text-blue-600 mb-1">
                                <i class="fas fa-spinner fa-spin mr-2"></i>
                                <span class="text-sm font-medium">Processing through LLM chain...</span>
                            </div>
                            <div class="mt-2 w-full bg-blue-100 rounded-full h-1.5">
                                <div class="bg-blue-600 h-1.5 rounded-full animate-pulse" style="width: 5%"></div>
                            </div>
                        </div>
                    </div>
                `;
                chatContainer.appendChild(processingDiv);
                
                // Scroll to bottom
                chatContainer.scrollTop = chatContainer.scrollHeight;
                
                // Simulate response after delay
                setTimeout(() => {
                    processingDiv.remove();
                    
                    const responseDiv = document.createElement('div');
                    responseDiv.className = 'flex justify-start';
                    responseDiv.innerHTML = `
                        <div class="max-w-3xl bg-white rounded-xl shadow-sm p-4">
                            <div class="flex items-center mb-2">
                                <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center mr-3">
                                    <i class="fas fa-robot text-indigo-600"></i>
                                </div>
                                <span class="font-medium text-gray-700">NexusFlow</span>
                            </div>
                            <p class="text-gray-700">I've processed your input through the LLM chain. Here's the refined output:</p>
                            <div class="mt-3 p-3 bg-gray-50 rounded-lg">
                                <p class="text-gray-700">${generateLLMResponse(message)}</p>
                            </div>
                            <div class="mt-4 flex space-x-2">
                                <button class="text-sm px-3 py-1 bg-indigo-50 text-indigo-600 rounded hover:bg-indigo-100">
                                    <i class="fas fa-redo mr-1"></i> Regenerate
                                </button>
                                <button class="text-sm px-3 py-1 bg-gray-100 text-gray-600 rounded hover:bg-gray-200">
                                    <i class="fas fa-edit mr-1"></i> Edit
                                </button>
                                <button class="text-sm px-3 py-1 bg-gray-100 text-gray-600 rounded hover:bg-gray-200">
                                    <i class="fas fa-code-branch mr-1"></i> Branch
                                </button>
                            </div>
                        </div>
                    `;
                    chatContainer.appendChild(responseDiv);
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }, 3000);
            }
        });

        // Generate a simulated LLM response
        function generateLLMResponse(input) {
            const responses = [
                `Based on your input "${input}", I've expanded the concept to include market analysis, technical requirements, and potential revenue streams. The expanded version now includes detailed user personas and a phased implementation plan.`,
                `Your idea about "${input}" has been enhanced with competitive analysis showing 3 major players in this space, along with a SWOT analysis and potential partnership opportunities.`,
                `The initial concept "${input}" has been developed into a comprehensive project plan including MVP features, technology stack recommendations, and a 6-month roadmap with key milestones.`,
                `After processing through our LLM chain, your input "${input}" now includes financial projections, risk assessment, and go-to-market strategy with channel recommendations.`
            ];
            return responses[Math.floor(Math.random() * responses.length)];
        }
    </script>
</body>
</html><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexusFlow - LLM Chain Automation Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .animate-pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
        .gradient-bg {
            background: linear-gradient(135deg, #6e8efb 0%, #a777e3 100%);
        }
        .chain-node {
            position: relative;
        }
        .chain-node:not(:last-child):after {
            content: "";
            position: absolute;
            right: -20px;
            top: 50%;
            width: 20px;
            height: 2px;
            background: #a0aec0;
        }
        .scrollbar-hide::-webkit-scrollbar {
            display: none;
        }
        .scrollbar-hide {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        .prompt-editor {
            min-height: 120px;
            border: 1px solid #e2e8f0;
            border-radius: 0.375rem;
            padding: 0.75rem;
        }
        .prompt-editor:focus {
            outline: none;
            border-color: #a777e3;
            box-shadow: 0 0 0 1px #a777e3;
        }
        .ollama-badge {
            background-color: #3B82F6;
            color: white;
        }
    </style>
</head>
<body class="bg-gray-50 h-screen flex overflow-hidden">
    <!-- Sidebar -->
    <div class="w-16 bg-white shadow-md flex flex-col items-center py-4">
        <div class="gradient-bg rounded-lg p-2 mb-6">
            <i class="fas fa-link text-white text-xl"></i>
        </div>
        <button id="chat-btn" class="w-12 h-12 rounded-lg mb-3 flex items-center justify-center bg-indigo-100 text-indigo-600">
            <i class="fas fa-comment-dots text-xl"></i>
        </button>
        <button id="chain-btn" class="w-12 h-12 rounded-lg mb-3 flex items-center justify-center hover:bg-gray-100 text-gray-600">
            <i class="fas fa-link text-xl"></i>
        </button>
        <button id="history-btn" class="w-12 h-12 rounded-lg mb-3 flex items-center justify-center hover:bg-gray-100 text-gray-600">
            <i class="fas fa-history text-xl"></i>
        </button>
        <div class="mt-auto">
            <button id="settings-btn" class="w-12 h-12 rounded-lg flex items-center justify-center hover:bg-gray-100 text-gray-600">
                <i class="fas fa-cog text-xl"></i>
            </button>
        </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Header -->
        <header class="bg-white shadow-sm py-3 px-6 flex items-center justify-between">
            <h1 class="text-xl font-semibold text-gray-800">NexusFlow</h1>
            <div class="flex items-center space-x-4">
                <div class="relative">
                    <button class="flex items-center space-x-2 bg-gray-100 hover:bg-gray-200 rounded-full px-4 py-1.5">
                        <span class="text-sm font-medium text-gray-700">New Session</span>
                        <i class="fas fa-plus text-gray-500"></i>
                    </button>
                </div>
                <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center">
                    <i class="fas fa-user text-indigo-600"></i>
                </div>
            </div>
        </header>

        <!-- Dynamic Content Area -->
        <div class="flex-1 overflow-hidden flex">
            <!-- Chat Interface (Default View) -->
            <div id="chat-view" class="flex-1 flex flex-col h-full">
                <!-- Chat Messages -->
                <div class="flex-1 overflow-y-auto p-6 space-y-4 scrollbar-hide">
                    <div class="flex justify-start">
                        <div class="max-w-3xl bg-white rounded-xl shadow-sm p-4">
                            <div class="flex items-center mb-2">
                                <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center mr-3">
                                    <i class="fas fa-robot text-indigo-600"></i>
                                </div>
                                <span class="font-medium text-gray-700">NexusFlow</span>
                            </div>
                            <p class="text-gray-700">Welcome to NexusFlow! I'm your LLM chain automation assistant. Start by entering your idea or question below, and I'll guide it through our optimized LLM processing pipeline.</p>
                        </div>
                    </div>
                    
                    <div class="flex justify-end">
                        <div class="max-w-3xl bg-indigo-50 rounded-xl shadow-sm p-4">
                            <div class="flex items-center mb-2">
                                <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center mr-3">
                                    <i class="fas fa-lightbulb text-indigo-600"></i>
                                </div>
                                <span class="font-medium text-gray-700">Initial Idea</span>
                            </div>
                            <p class="text-gray-700">I want to create an automated system that takes a basic product idea and develops it into a complete business plan using a chain of specialized LLMs.</p>
                        </div>
                    </div>
                    
                    <div class="flex justify-start">
                        <div class="max-w-3xl bg-white rounded-xl shadow-sm p-4">
                            <div class="flex items-center mb-2">
                                <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center mr-3">
                                    <i class="fas fa-robot text-indigo-600"></i>
                                </div>
                                <span class="font-medium text-gray-700">NexusFlow</span>
                            </div>
                            <p class="text-gray-700">Excellent! I'll process this through our 5-stage LLM chain:</p>
                            <div class="mt-3 flex space-x-2 overflow-x-auto pb-2">
                                <div class="chain-node flex flex-col items-center bg-indigo-50 rounded-lg p-3 min-w-[120px]">
                                    <div class="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center mb-2">
                                        <span class="text-indigo-600 font-bold">1</span>
                                    </div>
                                    <span class="text-xs font-medium text-gray-700">Concept Expansion</span>
                                </div>
                                <div class="chain-node flex flex-col items-center bg-indigo-50 rounded-lg p-3 min-w-[120px]">
                                    <div class="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center mb-2">
                                        <span class="text-indigo-600 font-bold">2</span>
                                    </div>
                                    <span class="text-xs font-medium text-gray-700">Market Analysis</span>
                                </div>
                                <div class="chain-node flex flex-col items-center bg-indigo-50 rounded-lg p-3 min-w-[120px]">
                                    <div class="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center mb-2">
                                        <span class="text-indigo-600 font-bold">3</span>
                                    </div>
                                    <span class="text-xs font-medium text-gray-700">Technical Feasibility</span>
                                </div>
                                <div class="chain-node flex flex-col items-center bg-indigo-50 rounded-lg p-3 min-w-[120px]">
                                    <div class="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center mb-2">
                                        <span class="text-indigo-600 font-bold">4</span>
                                    </div>
                                    <span class="text-xs font-medium text-gray-700">Business Model</span>
                                </div>
                                <div class="chain-node flex flex-col items-center bg-indigo-50 rounded-lg p-3 min-w-[120px]">
                                    <div class="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center mb-2">
                                        <span class="text-indigo-600 font-bold">5</span>
                                    </div>
                                    <span class="text-xs font-medium text-gray-700">Final Proposal</span>
                                </div>
                            </div>
                            <div class="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
                                <div class="flex items-center text-blue-600 mb-1">
                                    <i class="fas fa-info-circle mr-2"></i>
                                    <span class="text-sm font-medium">Processing Stage 1/5</span>
                                </div>
                                <p class="text-sm text-blue-800">Expanding your initial concept with market research and potential applications...</p>
                                <div class="mt-2 w-full bg-blue-100 rounded-full h-1.5">
                                    <div class="bg-blue-600 h-1.5 rounded-full animate-pulse" style="width: 20%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Input Area -->
                <div class="border-t border-gray-200 p-4">
                    <div class="max-w-4xl mx-auto">
                        <div class="flex items-end space-x-2">
                            <div class="flex-1 bg-white rounded-lg shadow-sm border border-gray-200">
                                <div class="prompt-editor" contenteditable="true" placeholder="Enter your idea or question..."></div>
                                <div class="flex justify-between items-center px-3 py-2 border-t border-gray-100">
                                    <div class="flex space-x-2">
                                        <button class="w-8 h-8 rounded hover:bg-gray-100 flex items-center justify-center text-gray-500">
                                            <i class="fas fa-paperclip"></i>
                                        </button>
                                        <button class="w-8 h-8 rounded hover:bg-gray-100 flex items-center justify-center text-gray-500">
                                            <i class="fas fa-magic"></i>
                                        </button>
                                    </div>
                                    <button class="text-sm text-gray-500 hover:text-gray-700">
                                        <i class="fas fa-sliders-h mr-1"></i> Advanced
                                    </button>
                                </div>
                            </div>
                            <button class="w-12 h-12 rounded-lg gradient-bg text-white flex items-center justify-center shadow-md hover:shadow-lg transition-shadow">
                                <i class="fas fa-paper-plane text-xl"></i>
                            </button>
                        </div>
                        <p class="text-xs text-gray-500 mt-2 px-1">NexusFlow will process your input through the configured LLM chain. <a href="#" class="text-indigo-600 hover:underline">Edit chain configuration</a></p>
                    </div>
                </div>
            </div>

            <!-- Settings View (Hidden by default) -->
            <div id="settings-view" class="hidden flex-1 flex flex-col h-full bg-white">
                <div class="border-b border-gray-200 px-6 py-4">
                    <h2 class="text-lg font-semibold text-gray-800">Settings & Configuration</h2>
                    <p class="text-sm text-gray-500">Manage your API keys and LLM chain settings</p>
                </div>
                
                <div class="flex-1 overflow-y-auto p-6">
                    <div class="max-w-4xl mx-auto space-y-8">
                        <!-- API Keys Section -->
                        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                            <div class="border-b border-gray-200 px-5 py-4 bg-gray-50">
                                <h3 class="font-medium text-gray-800">LLM Provider API Keys</h3>
                                <p class="text-sm text-gray-500 mt-1">Configure access to different LLM providers in your chain</p>
                            </div>
                            <div class="divide-y divide-gray-200">
                                <!-- OpenAI -->
                                <div class="p-5">
                                    <div class="flex items-center justify-between mb-3">
                                        <div class="flex items-center">
                                            <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center mr-3">
                                                <i class="fab fa-openai text-gray-700"></i>
                                            </div>
                                            <div>
                                                <h4 class="font-medium text-gray-800">OpenAI</h4>
                                                <p class="text-xs text-gray-500">GPT-4, GPT-3.5 models</p>
                                            </div>
                                        </div>
                                        <div class="flex items-center space-x-2">
                                            <span class="text-xs px-2 py-1 rounded bg-green-100 text-green-800">Active</span>
                                            <button class="text-gray-400 hover:text-gray-600">
                                                <i class="fas fa-ellipsis-v"></i>
                                            </button>
                                        </div>
                                    </div>
                                    <div class="pl-13">
                                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <label class="block text-sm font-medium text-gray-700 mb-1">API Key</label>
                                                <div class="relative">
                                                    <input type="password" value="sk-********************" class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 pr-10">
                                                    <button class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600">
                                                        <i class="far fa-eye"></i>
                                                    </button>
                                                </div>
                                            </div>
                                            <div>
                                                <label class="block text-sm font-medium text-gray-700 mb-1">Organization</label>
                                                <input type="text" value="org-****************" class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                                            </div>
                                        </div>
                                        <div class="mt-3 flex items-center justify-between">
                                            <div class="flex items-center space-x-2">
                                                <div class="w-2 h-2 rounded-full bg-green-500"></div>
                                                <span class="text-xs text-gray-500">Last used: 5 min ago</span>
                                            </div>
                                            <button class="text-sm text-indigo-600 hover:text-indigo-800">Test Connection</button>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Anthropic -->
                                <div class="p-5">
                                    <div class="flex items-center justify-between mb-3">
                                        <div class="flex items-center">
                                            <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center mr-3">
                                                <i class="fas fa-robot text-gray-700"></i>
                                            </div>
                                            <div>
                                                <h4 class="font-medium text-gray-800">Anthropic</h4>
                                                <p class="text-xs text-gray-500">Claude models</p>
                                            </div>
                                        </div>
                                        <div class="flex items-center space-x-2">
                                            <span class="text-xs px-2 py-1 rounded bg-yellow-100 text-yellow-800">Not Configured</span>
                                            <button class="text-gray-400 hover:text-gray-600">
                                                <i class="fas fa-ellipsis-v"></i>
                                            </button>
                                        </div>
                                    </div>
                                    <div class="pl-13">
                                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <label class="block text-sm font-medium text-gray-700 mb-1">API Key</label>
                                                <div class="relative">
                                                    <input type="password" placeholder="Enter your API key" class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 pr-10">
                                                    <button class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600">
                                                        <i class="far fa-eye"></i>
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="mt-3 flex items-center justify-end">
                                            <button class="text-sm text-indigo-600 hover:text-indigo-800">Test Connection</button>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Ollama -->
                                <div class="p-5">
                                    <div class="flex items-center justify-between mb-3">
                                        <div class="flex items-center">
                                            <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center mr-3">
                                                <i class="fas fa-server text-gray-700"></i>
                                            </div>
                                            <div>
                                                <h4 class="font-medium text-gray-800">Ollama</h4>
                                                <p class="text-xs text-gray-500">Local LLM models</p>
                                            </div>
                                        </div>
                                        <div class="flex items-center space-x-2">
                                            <span class="text-xs px-2 py-1 rounded bg-blue-100 text-blue-800 ollama-badge">Self-Hosted</span>
                                            <button class="text-gray-400 hover:text-gray-600">
                                                <i class="fas fa-ellipsis-v"></i>
                                            </button>
                                        </div>
                                    </div>
                                    <div class="pl-13">
                                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <label class="block text-sm font-medium text-gray-700 mb-1">Base URL</label>
                                                <input type="text" value="http://localhost:11434" class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                                            </div>
                                            <div>
                                                <label class="block text-sm font-medium text-gray-700 mb-1">Model</label>
                                                <select class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                                                    <option>llama3</option>
                                                    <option>mistral</option>
                                                    <option>gemma</option>
                                                    <option>phi3</option>
                                                    <option selected>Custom Model</option>
                                                </select>
                                            </div>
                                        </div>
                                        <div class="mt-4">
                                            <label class="block text-sm font-medium text-gray-700 mb-1">Custom Model Name</label>
                                            <input type="text" placeholder="my-custom-model" class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                                        </div>
                                        <div class="mt-3 flex items-center justify-between">
                                            <div class="flex items-center space-x-2">
                                                <div class="w-2 h-2 rounded-full bg-green-500"></div>
                                                <span class="text-xs text-gray-500">Connected to local Ollama instance</span>
                                            </div>
                                            <button class="text-sm text-indigo-600 hover:text-indigo-800">Test Connection</button>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Add New Provider -->
                                <div class="p-5">
                                    <button class="w-full flex items-center justify-center space-x-2 text-indigo-600 hover:text-indigo-800 py-2 rounded-md border-2 border-dashed border-gray-300 hover:border-indigo-300">
                                        <i class="fas fa-plus"></i>
                                        <span>Add LLM Provider</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Chain Configuration -->
                        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                            <div class="border-b border-gray-200 px-5 py-4 bg-gray-50">
                                <h3 class="font-medium text-gray-800">LLM Chain Configuration</h3>
                                <p class="text-sm text-gray-500 mt-1">Define the sequence and parameters for your LLM processing chain</p>
                            </div>
                            <div class="p-5">
                                <div class="space-y-6">
                                    <!-- Chain Stages -->
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-2">Chain Stages</label>
                                        <div class="space-y-3">
                                            <!-- Stage 1 -->
                                            <div class="flex items-start space-x-3 p-3 bg-indigo-50 rounded-lg">
                                                <div class="flex-shrink-0 mt-1">
                                                    <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center">
                                                        <span class="text-indigo-600 font-bold">1</span>
                                                    </div>
                                                </div>
                                                <div class="flex-1 min-w-0">
                                                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                                        <div>
                                                            <label class="block text-xs font-medium text-gray-500 mb-1">LLM Provider</label>
                                                            <select class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                                <option>OpenAI GPT-4</option>
                                                                <option>OpenAI GPT-3.5</option>
                                                                <option>Anthropic Claude 3</option>
                                                                <option selected>Ollama Llama3</option>
                                                            </select>
                                                        </div>
                                                        <div>
                                                            <label class="block text-xs font-medium text-gray-500 mb-1">Temperature</label>
                                                            <input type="range" min="0" max="1" step="0.1" value="0.7" class="w-full">
                                                            <div class="flex justify-between text-xs text-gray-500 mt-1">
                                                                <span>Precise</span>
                                                                <span>Creative</span>
                                                            </div>
                                                        </div>
                                                        <div>
                                                            <label class="block text-xs font-medium text-gray-500 mb-1">Max Tokens</label>
                                                            <input type="number" value="1000" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                        </div>
                                                    </div>
                                                    <div class="mt-3">
                                                        <label class="block text-xs font-medium text-gray-500 mb-1">Custom Prompt Template</label>
                                                        <textarea rows="2" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">Expand the following concept with detailed explanations and potential applications: {input}</textarea>
                                                    </div>
                                                </div>
                                                <button class="text-gray-400 hover:text-gray-600">
                                                    <i class="fas fa-times"></i>
                                                </button>
                                            </div>
                                            
                                            <!-- Stage 2 -->
                                            <div class="flex items-start space-x-3 p-3 bg-indigo-50 rounded-lg">
                                                <div class="flex-shrink-0 mt-1">
                                                    <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center">
                                                        <span class="text-indigo-600 font-bold">2</span>
                                                    </div>
                                                </div>
                                                <div class="flex-1 min-w-0">
                                                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                                        <div>
                                                            <label class="block text-xs font-medium text-gray-500 mb-1">LLM Provider</label>
                                                            <select class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                                <option>OpenAI GPT-4</option>
                                                                <option selected>Anthropic Claude 3</option>
                                                                <option>OpenAI GPT-3.5</option>
                                                                <option>Ollama Mistral</option>
                                                            </select>
                                                        </div>
                                                        <div>
                                                            <label class="block text-xs font-medium text-gray-500 mb-1">Temperature</label>
                                                            <input type="range" min="0" max="1" step="0.1" value="0.5" class="w-full">
                                                            <div class="flex justify-between text-xs text-gray-500 mt-1">
                                                                <span>Precise</span>
                                                                <span>Creative</span>
                                                            </div>
                                                        </div>
                                                        <div>
                                                            <label class="block text-xs font-medium text-gray-500 mb-1">Max Tokens</label>
                                                            <input type="number" value="1200" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                        </div>
                                                    </div>
                                                    <div class="mt-3">
                                                        <label class="block text-xs font-medium text-gray-500 mb-1">Custom Prompt Template</label>
                                                        <textarea rows="2" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">Analyze the following concept for market potential and competitive landscape: {input}</textarea>
                                                    </div>
                                                </div>
                                                <button class="text-gray-400 hover:text-gray-600">
                                                    <i class="fas fa-times"></i>
                                                </button>
                                            </div>
                                        </div>
                                        <button class="mt-3 flex items-center text-sm text-indigo-600 hover:text-indigo-800">
                                            <i class="fas fa-plus mr-1"></i>
                                            <span>Add Stage</span>
                                        </button>
                                    </div>
                                    
                                    <!-- Context Management -->
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-2">Context Management</label>
                                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <label class="block text-xs font-medium text-gray-500 mb-1">Context Preservation</label>
                                                <select class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                    <option>Full Context (High Cost)</option>
                                                    <option selected>Summarized Context (Recommended)</option>
                                                    <option>Minimal Context</option>
                                                </select>
                                            </div>
                                            <div>
                                                <label class="block text-xs font-medium text-gray-500 mb-1">Summary Length</label>
                                                <input type="number" value="300" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                <p class="text-xs text-gray-500 mt-1">Tokens to preserve between stages</p>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <!-- Fallback Strategy -->
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-2">Fallback Strategy</label>
                                        <div class="space-y-2">
                                            <div class="flex items-center">
                                                <input id="fallback-enabled" type="checkbox" checked class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
                                                <label for="fallback-enabled" class="ml-2 block text-sm text-gray-700">Enable automatic fallback to alternative models</label>
                                            </div>
                                            <div class="pl-6">
                                                <div class="flex items-center">
                                                    <input id="retry-enabled" type="checkbox" checked class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
                                                    <label for="retry-enabled" class="ml-2 block text-sm text-gray-700">Retry failed stages (max attempts)</label>
                                                    <input type="number" value="3" class="ml-2 w-16 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                                                </div>
                                                <div class="mt-2 flex items-center">
                                                    <input id="ollama-fallback" type="checkbox" checked class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
                                                    <label for="ollama-fallback" class="ml-2 block text-sm text-gray-700">Use Ollama as fallback when cloud models fail</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Save Settings -->
                        <div class="flex justify-end space-x-3">
                            <button class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                                Reset
                            </button>
                            <button class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                                Save Changes
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Toggle between chat and settings view
        document.getElementById('chat-btn').addEventListener('click', function() {
            document.getElementById('chat-view').classList.remove('hidden');
            document.getElementById('settings-view').classList.add('hidden');
            document.getElementById('chat-btn').classList.add('bg-indigo-100', 'text-indigo-600');
            document.getElementById('chat-btn').classList.remove('hover:bg-gray-100', 'text-gray-600');
            document.getElementById('settings-btn').classList.remove('bg-indigo-100', 'text-indigo-600');
            document.getElementById('settings-btn').classList.add('hover:bg-gray-100', 'text-gray-600');
        });

        document.getElementById('settings-btn').addEventListener('click', function() {
            document.getElementById('chat-view').classList.add('hidden');
            document.getElementById('settings-view').classList.remove('hidden');
            document.getElementById('settings-btn').classList.add('bg-indigo-100', 'text-indigo-600');
            document.getElementById('settings-btn').classList.remove('hover:bg-gray-100', 'text-gray-600');
            document.getElementById('chat-btn').classList.remove('bg-indigo-100', 'text-indigo-600');
            document.getElementById('chat-btn').classList.add('hover:bg-gray-100', 'text-gray-600');
        });

        // Simulate chat functionality
        document.querySelector('.fa-paper-plane').addEventListener('click', function() {
            const promptEditor = document.querySelector('.prompt-editor');
            const message = promptEditor.textContent.trim();
            
            if (message) {
                // Add user message to chat
                const chatContainer = document.querySelector('#chat-view > div.flex-1');
                const userMessageDiv = document.createElement('div');
                userMessageDiv.className = 'flex justify-end';
                userMessageDiv.innerHTML = `
                    <div class="max-w-3xl bg-indigo-50 rounded-xl shadow-sm p-4">
                        <div class="flex items-center mb-2">
                            <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center mr-3">
                                <i class="fas fa-lightbulb text-indigo-600"></i>
                            </div>
                            <span class="font-medium text-gray-700">You</span>
                        </div>
                        <p class="text-gray-700">${message}</p>
                    </div>
                `;
                chatContainer.appendChild(userMessageDiv);
                
                // Clear input
                promptEditor.textContent = '';
                
                // Add processing indicator
                const processingDiv = document.createElement('div');
                processingDiv.className = 'flex justify-start';
                processingDiv.innerHTML = `
                    <div class="max-w-3xl bg-white rounded-xl shadow-sm p-4">
                        <div class="flex items-center mb-2">
                            <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center mr-3">
                                <i class="fas fa-robot text-indigo-600"></i>
                            </div>
                            <span class="font-medium text-gray-700">NexusFlow</span>
                        </div>
                        <div class="p-3 bg-blue-50 rounded-lg border border-blue-100">
                            <div class="flex items-center text-blue-600 mb-1">
                                <i class="fas fa-spinner fa-spin mr-2"></i>
                                <span class="text-sm font-medium">Processing through LLM chain...</span>
                            </div>
                            <div class="mt-2 w-full bg-blue-100 rounded-full h-1.5">
                                <div class="bg-blue-600 h-1.5 rounded-full animate-pulse" style="width: 5%"></div>
                            </div>
                        </div>
                    </div>
                `;
                chatContainer.appendChild(processingDiv);
                
                // Scroll to bottom
                chatContainer.scrollTop = chatContainer.scrollHeight;
                
                // Simulate response after delay
                setTimeout(() => {
                    processingDiv.remove();
                    
                    const responseDiv = document.createElement('div');
                    responseDiv.className = 'flex justify-start';
                    responseDiv.innerHTML = `
                        <div class="max-w-3xl bg-white rounded-xl shadow-sm p-4">
                            <div class="flex items-center mb-2">
                                <div class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center mr-3">
                                    <i class="fas fa-robot text-indigo-600"></i>
                                </div>
                                <span class="font-medium text-gray-700">NexusFlow</span>
                            </div>
                            <p class="text-gray-700">I've processed your input through the LLM chain. Here's the refined output:</p>
                            <div class="mt-3 p-3 bg-gray-50 rounded-lg">
                                <p class="text-gray-700">${generateLLMResponse(message)}</p>
                            </div>
                            <div class="mt-4 flex space-x-2">
                                <button class="text-sm px-3 py-1 bg-indigo-50 text-indigo-600 rounded hover:bg-indigo-100">
                                    <i class="fas fa-redo mr-1"></i> Regenerate
                                </button>
                                <button class="text-sm px-3 py-1 bg-gray-100 text-gray-600 rounded hover:bg-gray-200">
                                    <i class="fas fa-edit mr-1"></i> Edit
                                </button>
                                <button class="text-sm px-3 py-1 bg-gray-100 text-gray-600 rounded hover:bg-gray-200">
                                    <i class="fas fa-code-branch mr-1"></i> Branch
                                </button>
                            </div>
                        </div>
                    `;
                    chatContainer.appendChild(responseDiv);
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }, 3000);
            }
        });

        // Generate a simulated LLM response
        function generateLLMResponse(input) {
            const responses = [
                `Based on your input "${input}", I've expanded the concept to include market analysis, technical requirements, and potential revenue streams. The expanded version now includes detailed user personas and a phased implementation plan.`,
                `Your idea about "${input}" has been enhanced with competitive analysis showing 3 major players in this space, along with a SWOT analysis and potential partnership opportunities.`,
                `The initial concept "${input}" has been developed into a comprehensive project plan including MVP features, technology stack recommendations, and a 6-month roadmap with key milestones.`,
                `After processing through our LLM chain, your input "${input}" now includes financial projections, risk assessment, and go-to-market strategy with channel recommendations.`
            ];
            return responses[Math.floor(Math.random() * responses.length)];
        }
    </script>
</body>
</html>