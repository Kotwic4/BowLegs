const BACKEND_URL = "http://localhost:8888/api";

export const PICTURE_COLLECTION_URL = `${BACKEND_URL}/pictures`;
export const PICTURE_UPLOAD_URL = `${BACKEND_URL}/upload`;
export const PICTURE_SINGLE_URL = id => `${BACKEND_URL}/pictures/${id}`;
export const PICTURE_INPUT_URL = id => `${PICTURE_SINGLE_URL(id)}/input`;
export const PICTURE_MASK_URL = id => `${PICTURE_SINGLE_URL(id)}/mask`;
export const PICTURE_RESULT_URL = id => `${PICTURE_SINGLE_URL(id)}/result`;

export const get = (url) =>
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .catch(res => {
            throw res
        });

export const get_all_pictures = () => {
    return get(PICTURE_COLLECTION_URL);
};
