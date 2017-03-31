package RestFulServerTest;

import java.util.List;

import com.sun.research.ws.wadl.Response;

public class HttpResponseCode {
	public void checkHttpResponseCode(String url) {
		
	   // String url = "http://www.gmail.com";
		Response response =  given().get(url).then().extract().response();
		
 System.out.println(response.getStatus());
    }

	private Object given() {
		// TODO Auto-generated method stub
		return null;
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new HttpResponseCode().checkHttpResponseCode("http://www.gmail.com");

	}

}
