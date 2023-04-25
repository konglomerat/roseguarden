import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import VueCookies from 'vue-cookies';
import requestBuilder from '@/api/requestBuilder';

Vue.use(VueCookies, VueAxios, axios);

export default {
  namespaced: true,
  state: {
    actionlist: [],
    datalist: [],
    runner: 'uninitialized'

  },
  actions: {
    emitActionRequest({ commit, rootState, state, dispatch }, action, data = null) {
      let token = $cookies.get("user_jwt");//rootState.user.jwttoken;
      console.log("emitAction:", action, data, token,);
      let actionRequest = requestBuilder.newActionRequest(action, data);
      let options = {};
      if (token !== null) {
        options = {
          headers: { 'X-CSRF-TOKEN': token, 'Authorization': 'Bearer ' + token },
          withCredentials: true
        };
      }
      return new Promise((resolve, reject) => {
        axios
          .post("/api/v1", actionRequest, options)
          .then(r => r.data)
          .then(reply => {
            dispatch('updateApp', reply.head);
            for (let x of reply.actions) {
              switch (x.action) {
                case 'loadView':
                  this.dispatch('views/announceLoadView', [x.viewname]);
                  break;
              }
            }
            commit('addActions', { actions: reply.actions, data: reply.data });
            resolve(reply.response)
          })
          .catch(error => {
            console.log(error);
            if (error.response.status === 401) {
              this.dispatch('user/resetToken');
            }
            reject(error);
          });
      });
    },
    updateApp({ commit, rootState, state, dispatch }, head) {
      console.log((unescape(process.env.FRONTENDVERSION).toString()));
      rootState.app.backendVersion = head.version;
      rootState.app.frontendVersion = JSON.parse(unescape(process.env.FRONTENDVERSION).toString());
    },
    startRunner({ commit, state, dispatch }) {
      return new Promise((resolve, reject) => {
        console.log(state.runner)
        if (state.runner === 'uninitialized') {
          commit('setRunner', { runnerstate: 'idle' })
          dispatch('cycleRunner')
          console.log("Action runner started");
        } else {
          console.log("Action runner already started");
        }
        resolve();  // Let the calling function know that http is done. You may send some data back
      })
    },
    cycleRunner({ commit, state, dispatch }) {
      let timeout = 100;
      switch (state.runner) {
        case 'uninitialized':
          break;
        case 'idle':
          if (state.actionlist.length === 0) {
            break;
          } else {
            commit('setRunner', { runnerstate: 'running' })
            console.log("runner is running with ", state.actionlist.length, " new actions");
          }
        case 'running':
          if (state.actionlist.length === 0) {
            commit('setRunner', { runnerstate: 'idle' })
            console.log("runner is in idle");
            break;
          } else {
            commit('setRunner', { runnerstate: 'waiting' })
            dispatch('runAction', state.actionlist[0]);
          }
          break;
        case 'waiting':
          break;
        default:
          console.log("runner is in unhandled state");
          break;
      }
      let setTimeoutObject = setTimeout(() => {
        dispatch('cycleRunner');
      }, timeout);
    },
    runAction({ commit, state, dispatch }, action) {
      console.log(action);
      let setTimeoutObject = setTimeout(() => {
        switch (action.action) {
          case 'notify':
            this.dispatch('notifications/pushNotification', [action.message, action.messagetype]);
            break;
          case 'route':
            this.$router.push('/' + action.route);
            break;
          case 'updateActionlinkStatus':
            console.log("updateActionlinkStatus");
            this.dispatch('actionlink/pushStatus', [action.status, action.message]);
            break;
          case 'updateToken':
            this.dispatch('user/setToken', action.token);
            break;
          case 'updateMenu':
            this.dispatch('menu/updateMenu', action.data);
            break;
          case 'updateUserInfo':
            this.dispatch('user/setUserInfo', [action.firstname, action.lastname, action.mail]);
            break;
          case 'resetUserInfo':
            this.dispatch('user/resetUserInfo');
            break;
          case 'loadView':
            this.dispatch('views/loadView', [action.viewname, action.viewdata]);
            break;
          default:
            console.log("ingonore unknown action", action.action, "to handle");
            break;
        }
        Vue.nextTick(function () {
          commit('shiftActions');
          commit('setRunner', { runnerstate: 'running' });
        })
      }, action.delay * 1000);
    }
  },
  mutations: {
    setRunner(state, { runnerstate }) {
      state.runner = runnerstate;
    },
    addActions(state, { actions, data }) {
      state.actionlist = state.actionlist.concat(actions);
    },
    shiftActions(state) {
      state.actionlist.shift()
    }
  }
};