import React, {useEffect, useState} from 'react';
import {get_all_pictures} from "./utils/api";
import {Root} from "./components/Root";


const App = () => {
    const [data, setData] = useState([]);
    const [dataDict, setDataDict] = useState({});

    const addPictures = (pictures) => {
        const new_ids = new Set(pictures.map(e => e.id));
        const newData = data.filter(e => !new_ids.has(e.id));
        setData(newData.concat(pictures));
    };

    useEffect(() => {
        get_all_pictures().then(setData);
        const interval = setInterval(() => {
            get_all_pictures().then(setData);
        }, 30000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        setDataDict(data.reduce((map, obj) => {
            map[obj.id] = obj;
            return map;
        }, {}));
    }, [data]);

    return <Root data={data} dataDict={dataDict} addPictures={addPictures}/>

};

export default App;
