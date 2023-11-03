import axios from 'axios';

export function post(url, payload, onSuccess, onError) {
  axios.post(url, payload)
    .then((response) => {
      onSuccess()
    })
    .catch((error) => {
      console.log(error);
      onError()
    })
}

export function get(url, params, onSuccess, onError) {
	const _url  = new URL(url)
	_url.search = new URLSearchParams(params)

  axios.get(_url.toString())
    .then((response) => {
      onSuccess()
    })
    .catch((error) => {
      console.log(error);
      onError()
    })
}
