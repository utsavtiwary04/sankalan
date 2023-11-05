import axios from 'axios';

export function post(url, payload, onSuccess, onError) {
  axios.post(url, payload)
    .then((response) => {
      onSuccess(response)
    })
    .catch((error) => {
      onError(error)
    })
}

export function get(url, queryParams, onSuccess, onError) {
	const _url  = new URL(url)
	_url.search = new URLSearchParams(queryParams)

  axios.get(_url.toString())
    .then((response) => {
      onSuccess(response)
    })
    .catch((error) => {
      onError(error)
    })
}
