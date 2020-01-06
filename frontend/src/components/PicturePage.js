import {useParams} from "react-router";
import React from "react";
import CircularProgress from "@material-ui/core/CircularProgress";
import {makeStyles} from "@material-ui/core";
import Card from "@material-ui/core/Card";
import {PICTURE_INPUT_URL, PICTURE_MASK_URL, PICTURE_RESULT_URL} from "../utils/api";
import Typography from "@material-ui/core/Typography";
import CardContent from "@material-ui/core/CardContent";

const useStyles = makeStyles({
    card: {
        maxWidth: 345,
        minWidth: 100,
    },
    sectionContainer: {
        display: "flex",
        justifyContent: "space-around"
    },
    title: {
        fontSize: 14,
        textAlign: 'center'
    },
    mainTitle: {
        fontSize: 14,
    },
    body: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexGrow: '1',
    },
    cardContent: {
        display: 'flex',
        flexDirection: 'column',
        width: '100%',
        height: '100%',
    }
});

export const ImageSection = ({title, img}) => {

    const classes = useStyles();

    return (
        <Card className={classes.card} variant="outlined">
            <CardContent className={classes.cardContent}>
                <Typography className={classes.title} color="textSecondary" gutterBottom>
                    {title}
                </Typography>
                <Typography className={classes.body} component="div">
                    {img ? <img src={img} alt={title}/> : <CircularProgress/>}
                </Typography>
            </CardContent>
        </Card>
    )
};

export const PictureInfo = ({picture}) => {
    const classes = useStyles();

    const id = picture.id;

    const completed = picture.status == "Status.DONE";

    const status = completed ? "Done" : "Waiting";

    return (
        <div>
            <Typography className={classes.mainTitle} gutterBottom>
                id: {id}
                <br/>
                Status: {status}
            </Typography>
            <div className={classes.sectionContainer}>
                <ImageSection img={PICTURE_INPUT_URL(id)} title={'Input'}/>
                <ImageSection img={completed ? PICTURE_MASK_URL(id) : null} title={'Mask'}/>
                <ImageSection img={completed ? PICTURE_RESULT_URL(id) : null} title={'Result'}/>
            </div>
        </div>

    )
};


export const PicturePage = ({dataDict}) => {
    let {id} = useParams();

    if (dataDict[id]) {
        return <PictureInfo picture={dataDict[id]}/>
    } else {
        return <CircularProgress/>
    }
};