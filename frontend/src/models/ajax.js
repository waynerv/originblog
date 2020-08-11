function Request(url, prams, onsucceed, onfaill) {
  return new Promise((resolve,reject) => {
    url = url + '?' + Object.entries(prams).map(arr => arr[0] + '='+ arr[1]).join('&')
    let xhr = new XMLHttpRequest()
    xhr.open('GET', url, true)
    xhr.setRequestHeader("Authorization", localStorage.getItem('token'));
    xhr.onload = function() {
      if(xhr.status>=200 && xhr.status<300 || xhr.status===304){
        let result = JSON.parse(xhr.responseText)
        resolve(result)
        onsucceed()
      }else {
        onfaill(err=> reject(err))
      }
    }
      xhr.onerror = function(err) {
      console.log(err)
    }
    xhr.send()
  })
};

function Delete(url, prams, onsucceed, onfaill) {
  return new Promise((resolve,reject) => {
    url = url + '/' + prams 
    // Object.entries(prams).map(arr => arr[0] + '='+ arr[1]).join('&')
    let xhr = new XMLHttpRequest()
    xhr.open('DELETE', url, true)
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function() {
      if(xhr.status===204 ){
        resolve()
        onsucceed()
      }else {
        onfaill(err=> reject(err))
      }
    }
      xhr.onerror = function(err) {
      console.log(err)
    }
    xhr.send()
  })
};
function Update(url, id, prams, onsucceed, onfaill) {
  return new Promise((resolve,reject) => {
    url = url + '/' + id 
    // Object.entries(prams).map(arr => arr[0] + '='+ arr[1]).join('&')
    let xhr = new XMLHttpRequest()
    xhr.open('PUT', url, true)
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function() {
      if(xhr.status>=200 && xhr.status<300 || xhr.status===304 ){let result = JSON.parse(xhr.responseText)
      resolve(result)
      onsucceed()
      }else {
      onfaill(err=>reject(err))
      }
    }
    xhr.send(JSON.stringify(prams));
  })
};

function Post (url, data, onsucceed, onfaill) {
  return new Promise((resolve,reject) =>{
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function() {
      if(xhr.status>=200 && xhr.status<300 || xhr.status===304){
        let result = JSON.parse(xhr.responseText)
        resolve(result)
        onsucceed()
      }else {
        onfaill(err=>reject(err))
     }
   }
   xhr.send(JSON.stringify(data));
  })
  
};



export {
  Request, 
  Post,
  Delete,
  Update
}