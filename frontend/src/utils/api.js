const BACKEND_URL = process.env.API_URL || '/api' ;

export const PICTURE_COLLECTION_URL = `${BACKEND_URL}/pictures`;
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
    return get(PICTURE_COLLECTION_URL).then();
};

export const post_image = (url, file) => {
    const formData = new FormData();
    formData.append('file', file);

    const options = {
        method: 'POST',
        body: formData,
    };

    return fetch(url, options);
};

export const upload_image = (file) => {
    return post_image(PICTURE_COLLECTION_URL, file).then((response) => {
        return response.json();
    })
};

export const calc_img_compare = (id, file) => {
    return post_image(PICTURE_RESULT_URL(id), file)
};


export const calc_data_compare = (id, file) => {
    return post_image(PICTURE_MASK_URL(id), file).then((response) => {
        return response.json();
    })
};
