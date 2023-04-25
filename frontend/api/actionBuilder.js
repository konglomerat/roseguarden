export function newBaseAction() {
    let action = Object();
    action.action = 'undefined';
    action.workspace = 'undefined';
    action.version = 1.0;
    console.log("newBaseAction");
    return action;
}


// generic action to execute tasks or get data
export function newAction(workspace, workspaceAction, options = {}) {
    let action = newBaseAction();
    action.workspace = workspace;
    action.action = workspaceAction;
    action.version = 1.0;
    return { ...action, options };
}


// action to login with username and password
export function newLoginUserAction(username, password, options = {}) {
    let action = newBaseAction();
    action.action = 'login';
    action.workspace = 'users';
    action.version = 1.0;
    action.username = username;
    action.password = password;
    return { ...action, options };
}


// action send a lost password request
export function newLostPasswordAction(username, options = {}) {
    let action = newBaseAction();
    action.action = 'lostPassword';
    action.workspace = 'users';
    action.version = 1.0;
    action.username = username;
    return { ...action, options };
}

// action send a lost password request
export function newResendVerfificationMailAction(username, options = {}) {
    let action = newBaseAction();
    action.action = 'resendVerificationMail';
    action.workspace = 'users';
    action.version = 1.0;
    action.username = username;
    return { ...action, options };
}


// action to login with username and password
export function newResetPasswordAction(key, password, options = {}) {
    let action = newBaseAction();
    action.action = 'resetPassword';
    action.workspace = 'users';
    action.version = 1.0;
    action.resetKey = key;
    action.password = password;
    return { ...action, options };
}



// action to login with username and password
export function newRequestActionLinkAction(hash, options = {}) {
    let action = newBaseAction();
    action.action = 'runActionlink';
    action.workspace = 'users';
    action.version = 1.0;
    action.hash = hash;
    return { ...action, options };
}


// action to execute a data view action
export function newExecuteDataViewActionAction(workspace, view, viewaction, entry, options = {}) {
    let action = newBaseAction();
    action.action = 'executeViewAction';
    action.workspace = workspace;
    action.version = 1.0;
    action.view = view;
    action.viewAction = viewaction;
    action.entry = entry;
    return { ...action, options };
}

export function newChangePasswordAction(workspace, oldpassword, newpassword, options = {}) {
    let action = newBaseAction();
    action.action = 'changePassword';
    action.workspace = workspace;
    action.version = 1.0;
    action.oldpassword = oldpassword;
    action.newpassword = newpassword;
    return { ...action, options };
}

export function newAssignUserAuthenticatorAction(workspace, userId, authenticatorCode, options = {}) {
    let action = newBaseAction();
    action.action = 'assignUserAuthenticator';
    action.workspace = workspace;
    action.version = 1.0;
    action.userId = userId;
    action.authenticatorCode = authenticatorCode;
    return { ...action, options };
}

export function newAssignUserAuthenticatorWithRawKeysAction(workspace, userId, privateKey, publicKey, options = {}) {
    let action = newBaseAction();
    action.action = 'assignUserAuthenticatorWithRawKeys';
    action.workspace = workspace;
    action.version = 1.0;
    action.userId = userId;
    action.authenticatorPrivateKey = privateKey;
    action.authenticatorPublicKey = publicKey;
    return { ...action, options };
}

export function newUnassignUserAuthenticatorAction(workspace, userId, options = {}) {
    let action = newBaseAction();
    action.action = 'unassignUserAuthenticator';
    action.workspace = workspace;
    action.version = 1.0;
    action.userId = userId;
    return { ...action, options };
}



export function newChangePinAction(workspace, oldpassword, pin, options = {}) {
    let action = newBaseAction();
    action.action = 'changePin';
    action.workspace = workspace;
    action.version = 1.0;
    action.pin = pin;
    action.oldpassword = oldpassword;
    return { ...action, options };
}

export function newUpdateDataViewEntryAction(workspace, view, entry, options = {}) {
    let action = newBaseAction();
    action.action = 'updateViewEntry';
    action.workspace = workspace;
    action.version = 1.0;
    action.view = view;
    action.entry = entry;
    return { ...action, options };
}

// action to remove view entry
export function newRemoveDataViewEntryAction(workspace, view, entry = {}) {
    let action = newBaseAction();
    action.action = 'removeViewEntry';
    action.workspace = workspace;
    action.view = view;
    action.entry = entry;
    action.version = 1.0;
    return action;
}

// action to provide menu for user
export function newProvideMenuAction() {
    let action = newBaseAction();
    action.action = 'menu';
    action.workspace = 'users';
    action.version = 1.0;
    return action;
}

export function newProvideUserInfoAction() {
    let action = newBaseAction();
    action.action = 'userInfo';
    action.workspace = 'users';
    action.version = 1.0;
    return action;
}


// action to get specific view
export function newCreateViewAction(workspace, view, entry = {}) {
    let action = newBaseAction();
    action.action = 'createViewEntry';
    action.workspace = workspace;
    action.view = view;
    action.entry = entry;
    action.version = 1.0;
    return action;
}

// action to get specific view
export function newGetViewAction(workspace, view) {
    let action = newBaseAction();
    action.action = 'getView';
    action.workspace = workspace;
    action.view = view;
    action.version = 1.0;
    return action;
}

// action to login with username and password
export function newRegisterUserAction(userdata, options = {}) {
    let action = newBaseAction();
    action.action = 'register';
    action.workspace = 'users';
    action.version = 1.0;
    return { ...action, userdata, options };
}


// action to refresh the session token (jwt)
export function newRefreshUserAction() {
    let action = newBaseAction();
    action.workspace = 'users';
    action.action = 'refresh';
    action.version = 1.0;
    return action;
}

// action to logout and request a revoking
export function newLogoutuserAction() {
    let action = newBaseAction();
    action.workspace = 'users';
    action.action = 'logout';
    action.version = 1.0;
    return action;
}

// action to logout and request a revoking
export function newTriggerJobAction(jobId) {
    let action = newBaseAction();
    action.workspace = 'jobs';
    action.action = 'triggerJob';
    action.jobId = jobId
    action.version = 1.0;
    return action;
}

export function requestViewAction(workspace, view, action, item, actions) {
    let entry = { ...item };
    actions.forEach(element => delete entry[element.action]);
    let dataViewAction = [
        newExecuteDataViewActionAction(
            workspace,
            view,
            action,
            entry
        )
    ];
    return dataViewAction;
}


/*
export default {
    newLoginUserAction,
    newRegisterUserAction,
    newRefreshUserAction,
    newLogoutuserAction,
    newProvideMenuAction,
    newGetViewAction,
    newCreateViewAction,
    newExecuteDataViewActionAction,
    newUpdateDataViewEntryAction,
    newRequestActionLinkAction,
    newLostPasswordAction
};*/
