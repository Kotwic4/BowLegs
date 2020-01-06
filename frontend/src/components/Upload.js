import React, {useState} from "react";
import {makeStyles} from "@material-ui/core";

import {DropzoneArea} from 'material-ui-dropzone'
import Button from "@material-ui/core/Button";

import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import CircularProgress from "@material-ui/core/CircularProgress";
import {green} from "@material-ui/core/colors";
import {upload_image} from "../utils/api";
import Typography from "@material-ui/core/Typography";
import {Link} from "react-router-dom";

const useStyles = makeStyles(theme => ({
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
}));

export const NewPictureLink = ({picture}) => {

    const id = picture.id;

    return (
        <div>
            <Typography gutterBottom>
                New picture uploaded with id: <Link to={`/picture/${id}`}>{id}</Link>
            </Typography>
        </div>

    )
};

export const Upload = ({addPictures}) => {
    const classes = useStyles();

    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState();

    const filePresent = files.length > 0;

    const upload = () => {
        if (!loading && filePresent) {
            setLoading(true);
            upload_image(files[0]).then(r => {
                    setLoading(false);
                    setResult(r);
                    addPictures([r])
                }
            );
        }
    };

    return (
        <>
            {result ? <NewPictureLink picture={result}/> : ''}
            <div className={classes.root}>
                <div className={classes.wrapper}>
                    <Button
                        variant="contained"
                        color="primary"
                        className={classes.button}
                        disabled={loading || !filePresent}
                        onClick={upload}
                        startIcon={<CloudUploadIcon/>}
                    >
                        Upload
                    </Button>
                    {loading && <CircularProgress size={24} className={classes.buttonProgress}/>}
                </div>
            </div>
            <DropzoneArea
                onChange={setFiles}
                filesLimit={1}
                acceptedFiles={['image/*']}
                showPreviews={false}
                showPreviewsInDropzone={true}
                showFileNamesInPreview={true}
                showFileNames={true}
            />
        </>
    )
};
