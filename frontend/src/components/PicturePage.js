import {useParams} from "react-router";
import React, {useState} from "react";
import CircularProgress from "@material-ui/core/CircularProgress";
import {makeStyles} from "@material-ui/core";
import Card from "@material-ui/core/Card";
import {
    calc_data_compare,
    calc_img_compare,
    PICTURE_INPUT_URL,
    PICTURE_MASK_URL,
    PICTURE_RESULT_URL
} from "../utils/api";
import Typography from "@material-ui/core/Typography";
import CardContent from "@material-ui/core/CardContent";
import Button from "@material-ui/core/Button";
import {DropzoneArea} from "material-ui-dropzone";
import {green} from "@material-ui/core/colors";
import Fab from "@material-ui/core/Fab";
import DeleteIcon from '@material-ui/icons/Delete';

const useStyles = makeStyles(theme => ({
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
    },
    button: {
        margin: theme.spacing(1),
    },
    buttonProgress: {
        color: green[500],
        position: 'absolute',
        top: '50%',
        left: '50%',
        marginTop: -12,
        marginLeft: -12,
    },
    wrapper: {
        margin: theme.spacing(1),
        position: 'relative',
    },
    root: {
        display: 'flex',
        alignItems: 'center',
    },
    compareSection: {
        display: "flex",
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
    },
    removeBtn: {
        transition: '.5s ease',
        position: 'absolute',
        opacity: 0,
        top: -5,
        right: -5,
        width: 40,
        height: 40
    },
    PreviewImg: {
        // height: 100,
        // width: 'initial',
        // maxWidth: '100%',
        // marginTop: 5,
        // marginRight: 10,
        // color: 'rgba(0, 0, 0, 0.87)',
        // transition: 'all 450ms cubic-bezier(0.23, 1, 0.32, 1) 0ms',
        // boxSizing: 'border-box',
        // boxShadow: 'rgba(0, 0, 0, 0.12) 0 1px 6px, rgba(0, 0, 0, 0.12) 0 1px 4px',
        // borderRadius: 2,
        zIndex: 5,
        opacity: 1
    },
    imageContainer: {
        position: 'relative',
        zIndex: 10,
        textAlign: 'center',
        '&:hover $PreviewImg': {
            opacity: 0.3
        },
        '&:hover $removeBtn': {
            opacity: 1
        }
    }
}));

export const Section = ({title, children}) => {

    const classes = useStyles();

    return (
        <Card className={classes.card} variant="outlined">
            <CardContent className={classes.cardContent}>
                <Typography className={classes.title} color="textSecondary" gutterBottom>
                    {title}
                </Typography>
                <Typography className={classes.body} component="div">
                    {children}
                </Typography>
            </CardContent>
        </Card>
    )
};

export const ImageSection = ({title, img}) => {
    return (
        <Section title={title}>
            {img ? <img src={img} alt={title}/> : <CircularProgress/>}
        </Section>
    )
};

export const GTPreview = ({gt, setgt}) => {
    const classes = useStyles();

    return (
        <div className={classes.imageContainer}>
            <img src={URL.createObjectURL(gt)} alt={'Golden Source'} className={classes.PreviewImg}/>
            <Fab onClick={() => setgt([])}
                 aria-label="Delete"
                 className={classes.removeBtn}>
                <DeleteIcon/>
            </Fab>
        </div>
    )
};

export const PictureInfo = ({picture}) => {
    const classes = useStyles();

    const id = picture.id;
    const completed = picture.status === "Status.DONE";
    const status = completed ? "Done" : "Waiting";

    const [gts, setgt] = useState([]);
    const [loadingImgCompare, setLoadingImgCompare] = useState(false);
    const [imgCompare, setImgCompare] = useState();
    const [loadingDataCompare, setLoadingDataCompare] = useState(false);
    const [dataCompare, setDataCompare] = useState();


    const gtPresent = gts.length > 0;
    const gt = gts[0];

    const loading = loadingImgCompare || loadingDataCompare;

    const upload = () => {
        if (!loading && gtPresent) {
            setLoadingImgCompare(true);
            setLoadingDataCompare(true);
            calc_img_compare(id, gt).then(response => response.blob())
                .then(image => {
                    const url = URL.createObjectURL(image);
                    setLoadingImgCompare(false);
                    setImgCompare(url);
                });
            calc_data_compare(id, gt).then(r => {
                setLoadingDataCompare(false);
                setDataCompare(r);
            });
        }
    };


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
                <Section title={'Golden Source'}>
                    {gt ? <GTPreview gt={gt} setgt={setgt}/> : <DropzoneArea
                        onChange={setgt}
                        filesLimit={1}
                        acceptedFiles={['image/*']}
                        showPreviews={false}
                        showPreviewsInDropzone={true}
                        showFileNamesInPreview={true}
                        showFileNames={true}
                    />}
                </Section>
                <Section title={'Comparision'}>
                    <div className={classes.compareSection}>
                        {(!loading && imgCompare && gtPresent) ?
                            <div><img src={imgCompare} alt={'img compare'}/></div> : ''}
                        {(!loading && dataCompare && gtPresent) ? <div>Dice: {dataCompare.dice}</div> : ''}
                        {(!loading && dataCompare && gtPresent) ? <div>IoU: {dataCompare.iou}</div> : ''}
                        <div className={classes.root}>
                            <div className={classes.wrapper}>
                                <Button
                                    variant="contained"
                                    color="primary"
                                    className={classes.button}
                                    disabled={!completed || loading || !gtPresent}
                                    onClick={upload}
                                >
                                    Recalculate
                                </Button>
                                {loading && <CircularProgress size={24} className={classes.buttonProgress}/>}
                            </div>
                        </div>
                    </div>
                </Section>
            </div>
        </div>

    )
};


export const PicturePage = ({dataDict}) => {
    let {id} = useParams();

    if (dataDict[id]) {
        return <PictureInfo key={id} picture={dataDict[id]}/>
    } else {
        return <CircularProgress/>
    }
};