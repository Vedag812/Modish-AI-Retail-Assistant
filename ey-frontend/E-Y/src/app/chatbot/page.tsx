
'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Send, Bot, User, Loader2, ShoppingCart, Package, CreditCard, Truck, Gift, RotateCcw, Crown, LogIn } from 'lucide-react';
import { chat } from '@/ai/flows/chat';
import type { ChatMessage } from '@/ai/flows/types';
import { useCustomer } from '@/context/customer-context';
import Link from 'next/link';

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
      return `🛒 **[Sales Agent]** Welcome back, ${cust.name}! 🎉\n\n` +
        `💎 **Your Loyalty Status:** ${cust.loyalty_tier} (${cust.loyalty_points} points)\n\n` +
        `I'm your AI shopping assistant powered by 6 specialized agents:\n\n` +
        `🔍 **Recommendation Agent** - Find perfect products for you\n` +
        `📦 **Inventory Agent** - Check stock & reserve items\n` +
        `💳 **Payment Agent** - Process payments via Razorpay\n` +
        `🚚 **Fulfillment Agent** - Schedule deliveries\n` +
        `🎁 **Loyalty Agent** - Manage your ${cust.loyalty_points} loyalty points\n` +
        `🔄 **Post-Purchase Agent** - Handle returns & support\n\n` +
        `How can I help you today?`;
    }
    return '🛒 **[Sales Agent]** Hello! I\'m your AI shopping assistant powered by 6 specialized agents:\n\n🔍 **Recommendation Agent** - Find perfect products\n📦 **Inventory Agent** - Check stock & reserve items\n💳 **Payment Agent** - Process payments via Razorpay\n🚚 **Fulfillment Agent** - Schedule deliveries\n🎁 **Loyalty Agent** - Manage rewards & registration\n🔄 **Post-Purchase Agent** - Handle returns & support\n\nHow can I help you today?';
  };

  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'model', content: getWelcomeMessage() },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [hasSetCustomerWelcome, setHasSetCustomerWelcome] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // Update welcome message once customer is loaded
  useEffect(() => {
    if (!customerLoading && !hasSetCustomerWelcome) {
      setMessages([{ role: 'model', content: getWelcomeMessage(customer ?? undefined) }]);
      setHasSetCustomerWelcome(true);
    }
  }, [customer, customerLoading, hasSetCustomerWelcome]);

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

    const userMessage: ChatMessage = { role: 'user', content: input };
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
    } catch (error) {
      console.error('Chatbot error:', error);
      const errorMessage: ChatMessage = {
        role: 'model',
        content: '🛒 **[Sales Agent]** Sorry, I encountered an issue. Please try again.',
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('chatSessionId', newSessionId);
    setSessionId(newSessionId);
    const welcomeText = isAuthenticated && customer 
      ? `🛒 **[Sales Agent]** Hello ${customer.name}! Starting a fresh conversation. How can I help you today?`
      : '🛒 **[Sales Agent]** Hello! Starting a fresh conversation. How can I help you today?';
    setMessages([
      { role: 'model', content: welcomeText },
    ]);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] w-full max-w-4xl mx-auto">
      {/* Header */}
      <div className="bg-card border rounded-t-xl p-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary to-primary/60 flex items-center justify-center">
            <Bot className="h-5 w-5 text-white" />
          </div>
          <div>
            <h2 className="font-semibold">AI Shopping Assistant</h2>
            <p className="text-xs text-muted-foreground">Powered by 6 specialized agents</p>
          </div>
        </div>
        <Button variant="outline" size="sm" onClick={handleNewChat}>
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
                <Avatar className="h-10 w-10 border-2 border-primary/20">
                  <AvatarFallback className="bg-gradient-to-br from-primary to-primary/60 text-white">
                    <Bot className="h-5 w-5" />
                  </AvatarFallback>
                </Avatar>
                <div className="bg-muted/80 border border-border rounded-2xl rounded-tl-sm px-4 py-3">
                  <div className="flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span className="text-sm text-muted-foreground">Agents working...</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>
      </div>

      {/* Input */}
      <div className="bg-card border rounded-b-xl p-4">
        <form onSubmit={handleSendMessage} className="flex items-center gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about products, orders, returns..."
            className="flex-1 h-11"
            disabled={isLoading}
          />
          <Button 
            type="submit" 
            disabled={isLoading || !input.trim()}
            size="lg"
            className="h-11 px-6"
          >
            <Send className="h-4 w-4 mr-2" />
            Send
          </Button>
        </form>
        <p className="text-xs text-muted-foreground mt-2 text-center">
          Try: "Show me smart TVs" • "I want to buy SKU IND1080" • "Register me as new customer"
        </p>
      </div>
    </div>
  );
}
