import axios from "axios";
import { isProd } from "./common";

declare const __APP_DEBUG__: boolean;

const baseApiUrl = isProd
  ? location.protocol + "//api." + location.host.replace(/^www\./, "")
  : "https://api.ziliang.ninja";

const axiosMl = axios.create({
  baseURL: baseApiUrl + "/v1/ml",
});

axiosMl.defaults.headers.post["Content-Type"] = "multipart/form-data";

const axiosCorsProxy = axios.create({
  baseURL: baseApiUrl + "/v1/cors-proxy",
});

if (__APP_DEBUG__) {
  [axiosMl, axiosCorsProxy].forEach((instance) => {
    instance.interceptors.request.use((request) => {
      console.log("Starting Request", request);
      return request;
    });

    instance.interceptors.response.use((response) => {
      console.log("Response:", response);
      return response;
    });
  });
}

export { axiosMl, axiosCorsProxy };
