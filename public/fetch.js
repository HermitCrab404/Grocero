
let serverURL = "http://localhost:8080/";

let epochOffset = 0;
function getEpoch() {
  return Date.now() + epochOffset;
}
async function sendRequest(method, path, body, noFileType) {
  try {
    let sendData = {
      method: method,
      headers: {
        cache: "no-cache"
      }
    };
    if (noFileType != true) {
      sendData.headers["Content-Type"] = "application/json";
    }
    if (body != null) {
      if (typeof body == "object" && body instanceof FormData == false) {
        body = JSON.stringify(body);
      }
      sendData.body = body;
    }
    let token = localStorage.getItem("token");
    if (token != null) {
      token = JSON.parse(token);
      if (token.expires > Math.floor(Date.now() / 1000)) {
        sendData.headers.auth =
          localStorage.getItem("userID") + ";" + token.token;
      }
    }
    let response = await fetch(serverURL + path, sendData);
    let serverTimeMillisGMT = new Date(response.headers.get("Date")).getTime();
    let localMillisUTC = new Date().getTime();
    epochOffset = serverTimeMillisGMT - localMillisUTC;
    return [response.status, await response.text()];
  } catch (err) {
    console.log("FETCH ERROR: " + err);
    return [0, "Fetch Error"];
  }
}
// Product request
async function getProducts(term) {
  // Use access stored access token for product request
  let accessToken = authentication.getAccessToken();
  // Use stored locationId
  let locationId = localStorage.getItem("locationId");

  // Use locationId as filter (if) selected by user
  let searchByLocation = "";
  if (locationId) {
    searchByLocation = `filter.locationId=${locationId}&`;
  }
  // Building product URL
  // Base URL (https://api.kroger.com)
  // Version/Endpoint (/v1/products)
  // Query String (?filter.locationId=${locationId}&filter.term=${term})
  let productsUrl = `${
    config.apiBaseUrl
  }/v1/products?${searchByLocation}filter.term=${term}`;

  // Product request body
  let productsResponse = await fetch(productsUrl, {
    method: "GET",
    cache: "no-cache",
    headers: {
      Authorization: `bearer ${accessToken}`,
      "Content-Type": "application/json; charset=utf-8"
    }
  });

  // Return json object
  return productsResponse.json();
}