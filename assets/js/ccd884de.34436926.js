"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[413],{3905:(e,n,t)=>{t.d(n,{Zo:()=>s,kt:()=>k});var r=t(7294);function a(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function o(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function l(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?o(Object(t),!0).forEach((function(n){a(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):o(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function i(e,n){if(null==e)return{};var t,r,a=function(e,n){if(null==e)return{};var t,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)t=o[r],n.indexOf(t)>=0||(a[t]=e[t]);return a}(e,n);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)t=o[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(a[t]=e[t])}return a}var p=r.createContext({}),u=function(e){var n=r.useContext(p),t=n;return e&&(t="function"==typeof e?e(n):l(l({},n),e)),t},s=function(e){var n=u(e.components);return r.createElement(p.Provider,{value:n},e.children)},c="mdxType",d={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},m=r.forwardRef((function(e,n){var t=e.components,a=e.mdxType,o=e.originalType,p=e.parentName,s=i(e,["components","mdxType","originalType","parentName"]),c=u(t),m=a,k=c["".concat(p,".").concat(m)]||c[m]||d[m]||o;return t?r.createElement(k,l(l({ref:n},s),{},{components:t})):r.createElement(k,l({ref:n},s))}));function k(e,n){var t=arguments,a=n&&n.mdxType;if("string"==typeof e||a){var o=t.length,l=new Array(o);l[0]=m;var i={};for(var p in n)hasOwnProperty.call(n,p)&&(i[p]=n[p]);i.originalType=e,i[c]="string"==typeof e?e:a,l[1]=i;for(var u=2;u<o;u++)l[u]=t[u];return r.createElement.apply(null,l)}return r.createElement.apply(null,t)}m.displayName="MDXCreateElement"},8759:(e,n,t)=>{t.r(n),t.d(n,{contentTitle:()=>l,default:()=>c,frontMatter:()=>o,metadata:()=>i,toc:()=>p});var r=t(7462),a=(t(7294),t(3905));const o={title:"Installation"},l="Setup Roseguarden-Server",i={type:"mdx",permalink:"/roseguarden/setup",source:"@site/src/pages/setup.md",title:"Installation",description:"Es gibt mehrere Wege den Roseguarden-Server zum laufen zu bekommen:",frontMatter:{title:"Installation"}},p=[{value:"1. Docker for Development (recommended)",id:"1-docker-for-development-recommended",level:2},{value:"2. By using the release packages",id:"2-by-using-the-release-packages",level:2},{value:"3. By cloning or forking the roseguarden repository",id:"3-by-cloning-or-forking-the-roseguarden-repository",level:2},{value:"3.1. Run Backend after fresh clone:",id:"31-run-backend-after-fresh-clone",level:3}],u={toc:p},s="wrapper";function c(e){let{components:n,...t}=e;return(0,a.kt)(s,(0,r.Z)({},u,t,{components:n,mdxType:"MDXLayout"}),(0,a.kt)("h1",{id:"setup-roseguarden-server"},"Setup Roseguarden-Server"),(0,a.kt)("p",null,"Es gibt mehrere Wege den Roseguarden-Server zum laufen zu bekommen:"),(0,a.kt)("h2",{id:"1-docker-for-development-recommended"},"1. Docker for Development (recommended)"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},"run ",(0,a.kt)("inlineCode",{parentName:"li"},"docker-compose up -d")),(0,a.kt)("li",{parentName:"ul"},"change frontend/nuxt.config.js change proxy-targets to: target: http://backend:5000 for /api/v1 and /api/v1/log"),(0,a.kt)("li",{parentName:"ul"},"frontend is listening on localhost:3000"),(0,a.kt)("li",{parentName:"ul"},"backend is listening on localhost:8002 (e.g. for direct calls via insomnia)")),(0,a.kt)("p",null,"\ud83d\udca5 ",(0,a.kt)("strong",{parentName:"p"},"Note:")," the first command is caching an ",(0,a.kt)("inlineCode",{parentName:"p"},"npm install")," into a named docker volume, which is then used in docker-compose. If you change anything in package.json rerun the first command to update dependencies."),(0,a.kt)("h2",{id:"2-by-using-the-release-packages"},"2. By using the release packages"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},"Download and unzip the latest release ",(0,a.kt)("inlineCode",{parentName:"li"},"roseguarden-X.Y.Z")," ",(0,a.kt)("a",{parentName:"li",href:"https://gitlab.com/roseguarden/roseguarden/-/releases"},"here")),(0,a.kt)("li",{parentName:"ul"},"Go to the folder and run the following commands in a terminal",(0,a.kt)("ul",{parentName:"li"},(0,a.kt)("li",{parentName:"ul"},"Install the requirements with ",(0,a.kt)("inlineCode",{parentName:"li"},"pip3 -r requirements.txt")),(0,a.kt)("li",{parentName:"ul"},"Create a ",(0,a.kt)("inlineCode",{parentName:"li"},"config.ini")," with your settings (see ",(0,a.kt)("inlineCode",{parentName:"li"},"config.template"),")"),(0,a.kt)("li",{parentName:"ul"},"Run 'flask run'")))),(0,a.kt)("h2",{id:"3-by-cloning-or-forking-the-roseguarden-repository"},"3. By cloning or forking the roseguarden repository"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},"Clone or fork ",(0,a.kt)("a",{parentName:"li",href:"https://gitlab.com/roseguarden/roseguarden"},"https://gitlab.com/roseguarden/roseguarden")),(0,a.kt)("li",{parentName:"ul"},"Have a look in the ",(0,a.kt)("inlineCode",{parentName:"li"},"backend")," and ",(0,a.kt)("inlineCode",{parentName:"li"},"frontend")," folder for details to setup your development enviroment"),(0,a.kt)("li",{parentName:"ul"},"run ",(0,a.kt)("inlineCode",{parentName:"li"},"backend")," and ",(0,a.kt)("inlineCode",{parentName:"li"},"frontend")," from your development environment (e.g. we use vs code)",(0,a.kt)("ul",{parentName:"li"},(0,a.kt)("li",{parentName:"ul"},"start the backend with ",(0,a.kt)("inlineCode",{parentName:"li"},"flask run")," out of the ",(0,a.kt)("inlineCode",{parentName:"li"},"backend")," folder (see more datailed instructions below)"),(0,a.kt)("li",{parentName:"ul"},"start the frontend with ",(0,a.kt)("inlineCode",{parentName:"li"},"npm run dev")," out of the ",(0,a.kt)("inlineCode",{parentName:"li"},"frontend")," folder")))),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},"alternativly you can use the ",(0,a.kt)("inlineCode",{parentName:"li"},"script/pack.py"),"-script to build your own package and host it with an HTTP-server")),(0,a.kt)("h3",{id:"31-run-backend-after-fresh-clone"},"3.1. Run Backend after fresh clone:"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"cd backend")),(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"python3 -m venv .venv")),(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},". venv/bin/activate")),(0,a.kt)("li",{parentName:"ul"},"(venv) ",(0,a.kt)("inlineCode",{parentName:"li"},"pip install Flask")),(0,a.kt)("li",{parentName:"ul"},"(venv) ",(0,a.kt)("inlineCode",{parentName:"li"},"pip install -r requirements.txt")),(0,a.kt)("li",{parentName:"ul"},"(venv) ",(0,a.kt)("inlineCode",{parentName:"li"},"run flask"))))}c.isMDXComponent=!0}}]);