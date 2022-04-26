var url = `${process.env.VUE_APP_DOMAIN}`;
var demo = parseInt(`${process.env.VUE_APP_DEMOMODE}`);
if (url == undefined) url = "";
if (demo == undefined) demo = 0;
export const apiUrl = url;
export const demoMode = demo;
