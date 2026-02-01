import { NextRequest, NextResponse } from 'next/server';

// Proxy API requests to the backend
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ proxy?: string[] }> }
) {
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
  const awaitedParams = await params;
  const proxyPath = awaitedParams.proxy?.join('/') || '';

  // Ensure the path starts with /api if it's an API request
  const normalizedPath = proxyPath.startsWith('api/') ? proxyPath : `api/${proxyPath}`;
  const url = `${backendUrl}/${normalizedPath}${request.nextUrl.search}`;

  // Get the authorization header from the original request
  const authHeader = request.headers.get('authorization');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (authHeader) {
    headers.Authorization = authHeader;
  }

  try {
    console.log('Proxy: Forwarding GET request to:', url);
    console.log('Proxy: Headers:', headers);

    const response = await fetch(url, {
      method: 'GET',
      headers: headers,
    });

    console.log('Proxy: Backend response status:', response.status);

    const responseBody = await response.text(); // Get response as text first

    return new Response(responseBody, {
      status: response.status,
      headers: response.headers,
    });
  } catch (error) {
    console.error('Proxy error:', error);
    return new Response(JSON.stringify({ error: 'Proxy request failed', details: (error as Error).message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ proxy?: string[] }> }
) {
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
  const awaitedParams = await params;
  const proxyPath = awaitedParams.proxy?.join('/') || '';

  // Ensure the path starts with /api if it's an API request
  const normalizedPath = proxyPath.startsWith('api/') ? proxyPath : `api/${proxyPath}`;
  const url = `${backendUrl}/${normalizedPath}`;
  const body = await request.json();

  // Get the authorization header from the original request
  const authHeader = request.headers.get('authorization');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (authHeader) {
    headers.Authorization = authHeader;
  }

  try {
    console.log('Proxy: Forwarding POST request to:', url);
    console.log('Proxy: Headers:', headers);
    console.log('Proxy: Body:', body);

    const response = await fetch(url, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(body),
    });

    console.log('Proxy: Backend response status:', response.status);

    const responseBody = await response.text(); // Get response as text first

    return new Response(responseBody, {
      status: response.status,
      headers: response.headers,
    });
  } catch (error) {
    console.error('Proxy error:', error);
    return new Response(JSON.stringify({ error: 'Proxy request failed', details: (error as Error).message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ proxy?: string[] }> }
) {
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
  const awaitedParams = await params;
  const proxyPath = awaitedParams.proxy?.join('/') || '';

  // Ensure the path starts with /api if it's an API request
  const normalizedPath = proxyPath.startsWith('api/') ? proxyPath : `api/${proxyPath}`;
  const url = `${backendUrl}/${normalizedPath}`;
  const body = await request.json();

  // Get the authorization header from the original request
  const authHeader = request.headers.get('authorization');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (authHeader) {
    headers.Authorization = authHeader;
  }

  try {
    console.log('Proxy: Forwarding PUT request to:', url);
    console.log('Proxy: Headers:', headers);
    console.log('Proxy: Body:', body);

    const response = await fetch(url, {
      method: 'PUT',
      headers: headers,
      body: JSON.stringify(body),
    });

    console.log('Proxy: Backend response status:', response.status);

    const responseBody = await response.text(); // Get response as text first

    return new Response(responseBody, {
      status: response.status,
      headers: response.headers,
    });
  } catch (error) {
    console.error('Proxy error:', error);
    return new Response(JSON.stringify({ error: 'Proxy request failed', details: (error as Error).message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ proxy?: string[] }> }
) {
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
  const awaitedParams = await params;
  const proxyPath = awaitedParams.proxy?.join('/') || '';

  // Ensure the path starts with /api if it's an API request
  const normalizedPath = proxyPath.startsWith('api/') ? proxyPath : `api/${proxyPath}`;
  const url = `${backendUrl}/${normalizedPath}`;

  // Get the authorization header from the original request
  const authHeader = request.headers.get('authorization');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (authHeader) {
    headers.Authorization = authHeader;
  }

  try {
    console.log('Proxy: Forwarding DELETE request to:', url);
    console.log('Proxy: Headers:', headers);

    const response = await fetch(url, {
      method: 'DELETE',
      headers: headers,
    });

    console.log('Proxy: Backend response status:', response.status);

    const responseBody = await response.text(); // Get response as text first

    return new Response(responseBody, {
      status: response.status,
      headers: response.headers,
    });
  } catch (error) {
    console.error('Proxy error:', error);
    return new Response(JSON.stringify({ error: 'Proxy request failed', details: (error as Error).message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}