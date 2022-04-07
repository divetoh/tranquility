import axios from "axios";
import { getLocalToken } from "@/utils";
import { apiUrl } from "@/env";

function authHeaders(token) {
  if (token === undefined) token = getLocalToken();
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

function make_URL_param(url_param) {
  var param = [];
  for (var i in url_param) param.push(`${i}=${url_param[i]}`);
  return "?" + param.join("&");
}

class APIBase {
  constructor(resource) {
    this.path = `${apiUrl}/api/v1/${resource}/`;
  }
  async get(uid, url_param) {
    const param = url_param == undefined ? "" : make_URL_param(url_param);
    return axios.get(this.path + uid + param, authHeaders());
  }
  async get_all(url_param) {
    const param = url_param == undefined ? "" : make_URL_param(url_param);
    return axios.get(this.path + param, authHeaders());
  }
  async delete(uid, url_param) {
    const param = url_param == undefined ? "" : make_URL_param(url_param);
    return axios.delete(this.path + uid + param, authHeaders());
  }
  async update(uid, data, url_param) {
    const param = url_param == undefined ? "" : make_URL_param(url_param);
    return axios.put(this.path + uid + param, data, authHeaders());
  }
  async create(data, url_param) {
    const param = url_param == undefined ? "" : make_URL_param(url_param);
    return axios.post(this.path + param, data, authHeaders());
  }
}

export const api = {
  user: new APIBase("users"),
  markdown: new APIBase("markdown"),
  regulartask: new APIBase("regulartask"),
  dailytask: new APIBase("dailytask"),
  jsondoc: new APIBase("jsondoc"),
  daystate: new APIBase("daystate"),
  regulartaskstate: new APIBase("regulartaskstate"),
  dailytaskstate: new APIBase("dailytaskstate"),

  async logInGetToken(username, password) {
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async resetPassword(password, token) {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
};
