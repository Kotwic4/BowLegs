import {BrowserRouter, Route, Switch} from "react-router-dom";
import {AppDrawer} from "./Drawer";
import {PictureList} from "./PictureList";
import React from "react";
import {PicturePage} from "./PicturePage";
import {Upload} from "./Upload";

export const Root = ({data, dataDict, addPictures}) => {
    return (
        <BrowserRouter>
            <AppDrawer
                drawer={<PictureList data={data}/>}
            >
                <Switch>
                    <Route path="/upload">
                        <Upload addPictures={addPictures}/>
                    </Route>
                    <Route path="/picture/:id">
                        <PicturePage dataDict={dataDict}/>
                    </Route>
                </Switch>
            </AppDrawer>
        </BrowserRouter>
    );
};
