
'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Send, Bot, User, Loader2, ShoppingCart, Package, CreditCard, Truck, Gift, RotateCcw, Crown, LogIn, Tv, Shirt, Smartphone, Search, Tag, ClipboardList, Mic, MicOff } from 'lucide-react';
import { chat } from '@/ai/flows/chat';
import type { ChatMessage } from '@/ai/flows/types';
import { useCustomer } from '@/context/customer-context';
import Link from 'next/link';

// Quick reply suggestions
const QUICK_REPLIES = [
  { id: 'menswear', label: '👔 Men\'s Fashion', message: 'Show me men\'s clothing', icon: Shirt },
  { id: 'womenswear', label: '👗 Women\'s Fashion', message: 'Show me women\'s clothing', icon: Shirt },
  { id: 'footwear', label: '👟 Footwear', message: 'Show me footwear options', icon: Shirt },
  { id: 'search', label: '🔍 Search Products', message: 'Help me search for products', icon: Search },
  { id: 'promo', label: '🏷️ Apply Promo', message: 'What promo codes are available?', icon: Tag },
  { id: 'track', label: '📦 Track Order', message: 'Track my order status', icon: ClipboardList },
];

// Agent configuration with colors and icons
const AGENTS = {
  'Sales Agent': { icon: ShoppingCart, color: 'bg-blue-500', emoji: '🛒' },
  'Recommendation Agent': { icon: Package, color: 'bg-purple-500', emoji: '🔍' },
  'Inventory Agent': { icon: Package, color: 'bg-green-500', emoji: '📦' },
  'Payment Agent': { icon: CreditCard, color: 'bg-yellow-500', emoji: '💳' },
  'Fulfillment Agent': { icon: Truck, color: 'bg-orange-500', emoji: '🚚' },
  'Loyalty Agent': { icon: Gift, color: 'bg-pink-500', emoji: '🎁' },
  'Post-Purchase Agent': { icon: RotateCcw, color: 'bg-red-500', emoji: '🔄' },
};

// Parse agent names from message content
function parseAgentMessage(content: string) {
  const agents: string[] = [];
  const agentPatterns = [
    /\*\*\[Sales Agent\]\*\*/g,
    /\*\*\[Recommendation Agent\]\*\*/g,
    /\*\*\[Inventory Agent\]\*\*/g,
    /\*\*\[Payment Agent\]\*\*/g,
    /\*\*\[Fulfillment Agent\]\*\*/g,
    /\*\*\[Loyalty Agent\]\*\*/g,
    /\*\*\[Post-Purchase Agent\]\*\*/g,
  ];
  
  const agentNames = ['Sales Agent', 'Recommendation Agent', 'Inventory Agent', 'Payment Agent', 'Fulfillment Agent', 'Loyalty Agent', 'Post-Purchase Agent'];
  
  agentNames.forEach((name, idx) => {
    if (agentPatterns[idx].test(content)) {
      agents.push(name);
    }
  });
  
  // Clean up the content - remove agent tags and emojis at start
  let cleanContent = content
    .replace(/🛒\s*\*\*\[Sales Agent\]\*\*/g, '')
    .replace(/🔍\s*\*\*\[Recommendation Agent\]\*\*/g, '')
    .replace(/📦\s*\*\*\[Inventory Agent\]\*\*/g, '')
    .replace(/💳\s*\*\*\[Payment Agent\]\*\*/g, '')
    .replace(/🚚\s*\*\*\[Fulfillment Agent\]\*\*/g, '')
    .replace(/🎁\s*\*\*\[Loyalty Agent\]\*\*/g, '')
    .replace(/🔄\s*\*\*\[Post-Purchase Agent\]\*\*/g, '')
    .replace(/\*\*\[Sales Agent\]\*\*/g, '')
    .replace(/\*\*\[Recommendation Agent\]\*\*/g, '')
    .replace(/\*\*\[Inventory Agent\]\*\*/g, '')
    .replace(/\*\*\[Payment Agent\]\*\*/g, '')
    .replace(/\*\*\[Fulfillment Agent\]\*\*/g, '')
    .replace(/\*\*\[Loyalty Agent\]\*\*/g, '')
    .replace(/\*\*\[Post-Purchase Agent\]\*\*/g, '')
    .trim();
  
  return { agents: agents.length > 0 ? agents : ['Sales Agent'], cleanContent };
}

// Agent badge component
function AgentBadge({ name }: { name: string }) {
  const config = AGENTS[name as keyof typeof AGENTS] || AGENTS['Sales Agent'];
  const Icon = config.icon;
  
  return (
    <div className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-full text-xs font-medium text-white ${config.color} mr-1 mb-1`}>
      <span>{config.emoji}</span>
      <span>{name}</span>
    </div>
  );
}

function ChatBubble({ message, customerName }: { message: ChatMessage; customerName?: string }) {
  const isUser = message.role === 'user';
  
  const getInitials = (name?: string | null) => {
    if (!name) return 'U';
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  };

  // Parse agent info from bot messages
  const { agents, cleanContent } = isUser 
    ? { agents: [], cleanContent: message.content }
    : parseAgentMessage(message.content);

  // Format markdown-like content and make links clickable
  const formatContent = (text: string) => {
    return text
      .replace(/\*\*Option (\d+):/g, '\n\n**Option $1:')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/⭐/g, '⭐ ')
      .replace(/₹/g, '₹')
      // Make URLs clickable - match https://... URLs
      .replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-blue-400 hover:text-blue-300 underline">$1</a>')
      .replace(/\n/g, '<br/>');
  };

  return (
    <div className={`flex items-start gap-3 ${isUser ? 'justify-end' : ''}`}>
      {!isUser && (
        <div className="flex-shrink-0">
          <Avatar className="h-10 w-10 border-2 border-primary/20">
            <AvatarFallback className="bg-gradient-to-br from-primary to-primary/60 text-white">
              <Bot className="h-5 w-5" />
            </AvatarFallback>
          </Avatar>
        </div>
      )}
      <div className={`max-w-[80%] ${isUser ? 'order-first' : ''}`}>
        {/* Agent badges */}
        {!isUser && agents.length > 0 && (
          <div className="flex flex-wrap mb-2">
            {agents.map((agent, idx) => (
              <AgentBadge key={idx} name={agent} />
            ))}
          </div>
        )}
        {/* Message bubble */}
        <div
          className={`rounded-2xl px-4 py-3 ${
            isUser 
              ? 'bg-primary text-primary-foreground rounded-tr-sm' 
              : 'bg-muted/80 border border-border rounded-tl-sm'
          }`}
        >
          <div 
            className="text-sm leading-relaxed"
            dangerouslySetInnerHTML={{ __html: formatContent(cleanContent) }}
          />
        </div>
      </div>
      {isUser && (
        <div className="flex-shrink-0">
          <Avatar className="h-10 w-10 border-2 border-primary/20">
            <AvatarFallback className="bg-gradient-to-br from-yellow-400 to-yellow-600 text-white font-semibold">
              {getInitials(customerName)}
            </AvatarFallback>
          </Avatar>
        </div>
      )}
    </div>
  );
}

export default function ChatbotPage() {
  const { customer, isAuthenticated, isLoading: customerLoading } = useCustomer();
  
  const getWelcomeMessage = (cust?: typeof customer) => {
    if (cust) {
      return `🛒 Welcome back, **${cust.name}**! 🎉\n\n` +
        `💎 **Your Loyalty Status:** ${cust.loyalty_tier} tier with ${cust.loyalty_points} points\n\n` +
        `I'm here to help you find the perfect fashion items, check availability, process payments, and manage your orders. Whether you're looking for men's wear, women's fashion, or footwear - I've got you covered!\n\n` +
        `**What would you like to do today?**\n` +
        `• Browse fashion categories\n` +
        `• Search for specific clothing items\n` +
        `• Check order status\n` +
        `• Apply loyalty rewards & promo codes\n\n` +
        `Just tell me what you need! 😊`;
    }
    return `👋 **Hello! Welcome to Modish!**\n\n` +
      `I'm your AI fashion assistant, ready to help you find exactly what you're looking for. From men's fashion to women's wear, footwear to accessories - we have it all!\n\n` +
      `**Here's what I can do for you:**\n` +
      `• 🔍 Find & recommend fashion items based on your style\n` +
      `• 📦 Check stock availability across warehouses\n` +
      `• 💳 Process secure payments via Razorpay\n` +
      `• 🚚 Schedule delivery to your location\n` +
      `• 🎁 Help you earn & redeem loyalty rewards\n` +
      `• 🔄 Assist with returns and exchanges\n\n` +
      `**New customer?** I can help you register and get 100 bonus loyalty points!\n\n` +
      `How can I assist you today? 😊`;
  };

  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'model', content: getWelcomeMessage() },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState(0);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [hasSetCustomerWelcome, setHasSetCustomerWelcome] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const loadingIntervalRef = useRef<NodeJS.Timeout | null>(null);
  
  // Loading stages for better UX
  const loadingMessages = [
    { text: 'Connecting to AI...', icon: '🔗' },
    { text: 'Analyzing your request...', icon: '🔍' },
    { text: 'Consulting style experts...', icon: '👔' },
    { text: 'Checking inventory...', icon: '📦' },
    { text: 'Almost there...', icon: '✨' },
  ];
  
  // Voice assistant state
  const [isListening, setIsListening] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  // Initialize speech recognition
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        setSpeechSupported(true);
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-IN';
        
        recognition.onresult = (event) => {
          const transcript = Array.from(event.results)
            .map(result => result[0])
            .map(result => result.transcript)
            .join('');
          setInput(transcript);
          
          // If this is a final result, auto-submit
          if (event.results[event.results.length - 1].isFinal) {
            setIsListening(false);
          }
        };
        
        recognition.onerror = (event) => {
          console.error('Speech recognition error:', event.error);
          setIsListening(false);
        };
        
        recognition.onend = () => {
          setIsListening(false);
        };
        
        recognitionRef.current = recognition;
      }
    }
    
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
    };
  }, []);

  const toggleVoiceInput = () => {
    if (!recognitionRef.current) return;
    
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      setInput('');
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  // Update welcome message once customer is loaded
  useEffect(() => {
    if (!customerLoading && !hasSetCustomerWelcome) {
      setMessages([{ role: 'model', content: getWelcomeMessage(customer ?? undefined) }]);
      setHasSetCustomerWelcome(true);
    }
  }, [customer, customerLoading, hasSetCustomerWelcome]);

  // Animate loading stages
  useEffect(() => {
    if (isLoading) {
      setLoadingStage(0);
      loadingIntervalRef.current = setInterval(() => {
        setLoadingStage(prev => (prev + 1) % loadingMessages.length);
      }, 2000);
    } else {
      if (loadingIntervalRef.current) {
        clearInterval(loadingIntervalRef.current);
        loadingIntervalRef.current = null;
      }
      setLoadingStage(0);
    }
    return () => {
      if (loadingIntervalRef.current) {
        clearInterval(loadingIntervalRef.current);
      }
    };
  }, [isLoading]);

  const scrollToBottom = () => {
    if (scrollAreaRef.current) {
      const viewport = scrollAreaRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (viewport) {
        viewport.scrollTop = viewport.scrollHeight;
      }
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Generate a persistent session ID
  useEffect(() => {
    const storedSessionId = localStorage.getItem('chatSessionId');
    if (storedSessionId) {
      setSessionId(storedSessionId);
    } else {
      const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('chatSessionId', newSessionId);
      setSessionId(newSessionId);
    }
  }, []);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    await sendMessage(input);
  };

  const sendMessage = async (messageText: string) => {
    if (!messageText.trim() || isLoading) return;

    const userMessage: ChatMessage = { role: 'user', content: messageText };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      const result = await chat({ 
        history: newMessages,
        sessionId: sessionId || undefined,
        customerId: customer?.customer_id,
      });
      
      // Update session ID if returned
      if (result.sessionId) {
        setSessionId(result.sessionId);
        localStorage.setItem('chatSessionId', result.sessionId);
      }
      
      const botMessage: ChatMessage = { role: 'model', content: result.message };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error: any) {
      console.error('Chatbot error:', error);
      const errorText = error?.message || String(error);
      let errorContent = '🛒 **[Sales Agent]** Sorry, I encountered an issue. Please try again.';
      
      if (errorText.includes('503') || errorText.includes('overloaded') || errorText.includes('UNAVAILABLE')) {
        errorContent = '⚡ **[Sales Agent]** Our AI is experiencing high demand right now. Please wait a moment and try again. Your request is important to us!';
      } else if (errorText.includes('timeout') || errorText.includes('TIMEOUT')) {
        errorContent = '⏱️ **[Sales Agent]** The request took too long. Please try a simpler question or try again.';
      }
      
      const errorMessage: ChatMessage = {
        role: 'model',
        content: errorContent,
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickReply = (message: string) => {
    sendMessage(message);
  };

  const handleNewChat = () => {
    const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('chatSessionId', newSessionId);
    setSessionId(newSessionId);
    const welcomeText = isAuthenticated && customer 
      ? `👋 Hello ${customer.name}! Ready to start fresh? What can I help you find today?`
      : '👋 Hello! Starting a new conversation. What can I help you with today?';
    setMessages([
      { role: 'model', content: welcomeText },
    ]);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)] sm:h-[calc(100vh-8rem)] w-full max-w-4xl mx-auto -mx-4 sm:mx-auto">
      {/* Header */}
      <div className="bg-card border sm:rounded-t-xl p-3 sm:p-4 flex items-center justify-between">
        <div className="flex items-center gap-2 sm:gap-3">
          <div className="h-8 w-8 sm:h-10 sm:w-10 rounded-full bg-gradient-to-br from-primary to-primary/60 flex items-center justify-center">
            <Bot className="h-4 w-4 sm:h-5 sm:w-5 text-white" />
          </div>
          <div>
            <h2 className="font-semibold text-sm sm:text-base">AI Shopping Assistant</h2>
            <p className="text-[10px] sm:text-xs text-muted-foreground">Your personal shopping companion</p>
          </div>
        </div>
        <Button variant="outline" size="sm" onClick={handleNewChat} className="text-xs sm:text-sm">
          New Chat
        </Button>
      </div>

      {/* Messages */}
      <div className="flex-1 bg-card/50 border-x overflow-hidden">
        <ScrollArea className="h-full p-4" ref={scrollAreaRef}>
          <div className="space-y-4 pb-4">
            {messages.map((message, index) => (
              <ChatBubble key={index} message={message} customerName={customer?.name} />
            ))}
            {isLoading && (
              <div className="flex items-start gap-3">
                <Avatar className="h-10 w-10 border-2 border-primary/20 animate-pulse">
                  <AvatarFallback className="bg-gradient-to-br from-primary to-primary/60 text-white">
                    <Bot className="h-5 w-5" />
                  </AvatarFallback>
                </Avatar>
                <div className="bg-muted/80 border border-border rounded-2xl rounded-tl-sm px-4 py-4 min-w-[200px]">
                  <div className="flex items-center gap-3">
                    <span className="text-lg">{loadingMessages[loadingStage].icon}</span>
                    <div>
                      <div className="flex items-center gap-2">
                        <Loader2 className="h-4 w-4 animate-spin text-primary" />
                        <span className="text-sm font-medium">{loadingMessages[loadingStage].text}</span>
                      </div>
                      <div className="flex gap-1 mt-2">
                        {loadingMessages.map((_, idx) => (
                          <div 
                            key={idx} 
                            className={`h-1 w-6 rounded-full transition-colors duration-300 ${
                              idx <= loadingStage ? 'bg-primary' : 'bg-muted-foreground/20'
                            }`}
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>
      </div>

      {/* Input */}
      <div className="bg-card border sm:rounded-b-xl p-3 sm:p-4">
        {/* Quick Reply Buttons - Scrollable on mobile */}
        <div className="flex gap-2 mb-3 overflow-x-auto pb-2 -mx-1 px-1 scrollbar-hide">
          {QUICK_REPLIES.map((reply) => {
            const IconComponent = reply.icon;
            return (
              <Button
                key={reply.id}
                variant="outline"
                size="sm"
                onClick={() => handleQuickReply(reply.message)}
                disabled={isLoading}
                className="h-8 text-xs font-medium hover:bg-primary/10 hover:border-primary/50 transition-colors whitespace-nowrap flex-shrink-0"
              >
                <IconComponent className="h-3.5 w-3.5 mr-1.5" />
                <span className="hidden sm:inline">{reply.label}</span>
                <span className="sm:hidden">{reply.label.split(' ')[0]}</span>
              </Button>
            );
          })}
        </div>

        <form onSubmit={handleSendMessage} className="flex items-center gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={isListening ? "🎤 Listening... Speak now" : "Ask about products..."}
            className={`flex-1 h-10 sm:h-11 text-sm transition-colors ${isListening ? 'border-red-500 bg-red-50 dark:bg-red-950/20' : ''}`}
            disabled={isLoading}
          />
          {speechSupported && (
            <Button 
              type="button"
              variant={isListening ? "destructive" : "outline"}
              size="lg"
              className={`h-10 sm:h-11 px-3 ${isListening ? 'animate-pulse' : ''}`}
              onClick={toggleVoiceInput}
              disabled={isLoading}
              title={isListening ? "Stop listening" : "Voice input"}
            >
              {isListening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
            </Button>
          )}
          <Button 
            type="submit" 
            disabled={isLoading || !input.trim()}
            size="lg"
            className="h-10 sm:h-11 px-3 sm:px-6"
          >
            <Send className="h-4 w-4 sm:mr-2" />
            <span className="hidden sm:inline">Send</span>
          </Button>
        </form>
        <p className="text-[10px] sm:text-xs text-muted-foreground mt-2 text-center">
          {speechSupported ? '💬 Type or 🎤 speak your question' : 'Type your question above'}
        </p>
      </div>
    </div>
  );
}
