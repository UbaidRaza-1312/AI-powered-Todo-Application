// Simple test to check backend connectivity
export async function GET(request: Request) {
  try {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
    const response = await fetch(`${backendUrl}/`);
    
    if (response.ok) {
      const data = await response.json();
      return Response.json({ 
        status: 'success', 
        message: 'Backend is accessible',
        backendResponse: data
      });
    } else {
      return Response.json({ 
        status: 'error', 
        message: 'Backend returned error',
        statusCode: response.status
      }, { status: 500 });
    }
  } catch (error) {
    console.error('Backend connectivity test failed:', error);
    return Response.json({ 
      status: 'error', 
      message: 'Cannot connect to backend',
      error: (error as Error).message
    }, { status: 500 });
  }
}