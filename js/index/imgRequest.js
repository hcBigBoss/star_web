
axios.defaults.baseURL = 'http://192.168.0.36:10086';

function getImgList(data){
    url = '/imgList'
    return  axios.post(url,data)

}

function getVideoList(data){
    url = '/videoList'
    return  axios.post(url,data)

}

