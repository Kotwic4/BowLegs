import React, {useEffect, useState} from 'react';
import {get_all_pictures} from "./utils/api";
import {Root} from "./components/Root";


const App = () => {
    const [data, setData] = useState([]);
    const [dataDict, setDataDict] = useState({});

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

    return <Root data={data} dataDict={dataDict}/>

};

export default App;
