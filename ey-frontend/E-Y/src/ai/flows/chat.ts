'use server';
/**
 * @fileOverview Chat flow that connects to the Python multi-agent backend
 * Replaces Genkit with calls to your FastAPI server running your 6 specialized agents
 */

import { z } from 'zod';
import { ChatMessageSchema } from './types';
import type { ChatMessage } from './types';

// API endpoint for your Python backend
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Define the schema for the chat flow input
const ChatInputSchema = z.object({
  history: z.array(ChatMessageSchema),
  sessionId: z.string().optional(),
  customerId: z.string().optional(),
});

// Define the schema for the chat flow output
const ChatOutputSchema = z.object({
  message: z.string(),
  sessionId: z.string().optional(),
  agentName: z.string().optional(),
});

/**
 * Sends the conversation history to your Python multi-agent backend
 * This connects to your 6 specialized agents:
 * - Recommendation Agent
 * - Inventory Agent  
 * - Payment Agent
 * - Fulfillment Agent
 * - Loyalty Agent
 * - Post-Purchase Agent
 */
export async function chat(
  input: z.infer<typeof ChatInputSchema>
): Promise<z.infer<typeof ChatOutputSchema>> {
  try {
    // Validate that we have history
    if (!input.history || input.history.length === 0) {
      return { message: "🛒 **[Sales Agent]** Hello! I'm your AI shopping assistant. How can I help you today?" };
    }

    // Call your Python FastAPI backend
    const response = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        history: input.history.map(msg => ({
          role: msg.role,
          content: msg.content,
        })),
        session_id: input.sessionId,
        customer_id: input.customerId,
      }),
      cache: 'no-store',
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Error:', errorText);
      return { 
        message: "🛒 **[Sales Agent]** I'm having trouble connecting. Please make sure the backend server is running.",
        sessionId: input.sessionId,
      };
    }

    const result = await response.json();
    
    // Use agent name from API response
    const agentName = result.agent_name || 'Sales Agent';
    const agentEmoji = {
      'Sales Agent': '🛒',
      'Loyalty Agent': '🎁',
      'Inventory Agent': '📦',
      'Payment Agent': '💳',
      'Fulfillment Agent': '🚚',
      'Post-Purchase Agent': '🔄',
      'Recommendation Agent': '🔍',
    }[agentName] || '🛒';
    
    // Prepend agent tag if not already present
    let messageWithAgent = result.message || "I'm here to help! What are you looking for?";
    if (!messageWithAgent.includes('**[')) {
      messageWithAgent = `${agentEmoji} **[${agentName}]** ${messageWithAgent}`;
    }
    
    return { 
      message: messageWithAgent,
      sessionId: result.session_id,
      agentName: agentName,
    };
  } catch (error) {
    console.error('Chat error:', error);
    
    // Check if it's a connection error
    if (error instanceof TypeError && error.message.includes('fetch')) {
      return { 
        message: "🛒 **[Sales Agent]** ⚠️ Cannot connect to the AI backend. Please start the server with: python api_server.py",
        sessionId: input.sessionId,
      };
    }
    
    return { 
      message: "🛒 **[Sales Agent]** I apologize, something went wrong. Please try again.",
      sessionId: input.sessionId,
    };
  }
}
