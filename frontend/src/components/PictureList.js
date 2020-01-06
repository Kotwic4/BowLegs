import React, {useEffect, useState} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Collapse from '@material-ui/core/Collapse';
import InboxIcon from '@material-ui/icons/MoveToInbox';
import DraftsIcon from '@material-ui/icons/Drafts';
import ExpandLess from '@material-ui/icons/ExpandLess';
import PublishIcon from '@material-ui/icons/Publish';
import ExpandMore from '@material-ui/icons/ExpandMore';
import {Star, StarHalf} from "@material-ui/icons";
import {Link} from "react-router-dom";

const useStyles = makeStyles(theme => ({
    root: {
        width: '100%',
        maxWidth: 360,
        backgroundColor: theme.palette.background.paper,
    },
    nested: {
        paddingLeft: theme.spacing(4),
    },
    nestedText: {
        whiteSpace: "nowrap",
        overflow: "hidden",
        textOverflow: "ellipsis",
    }
}));

const ExpandList = ({icon, title, data, positionIcon}) => {

    const classes = useStyles();

    const [open, setOpen] = React.useState(false);

    const handleClick = () => {
        setOpen(!open);
    };

    return (
        <>
            <ListItem button onClick={handleClick}>
                <ListItemIcon>
                    {icon}
                </ListItemIcon>
                <ListItemText primary={title}/>
                {open ? <ExpandLess/> : <ExpandMore/>}
            </ListItem>
            <Collapse in={open} timeout="auto" unmountOnExit>
                <List component="div" disablePadding>
                    {data.map(e => (
                        <ListItem button className={classes.nested}
                                  component={props => <Link to={`/picture/${e.id}`} {...props} />}>
                            <ListItemIcon>
                                {positionIcon}
                            </ListItemIcon>
                            <ListItemText className={classes.nestedText} primary={e.id}/>
                        </ListItem>
                    ))}
                </List>
            </Collapse>
        </>
    );
};

export const PictureList = ({data}) => {
    const classes = useStyles();

    const [waitData, setWaitData] = useState([]);
    const [doneData, setDoneData] = useState([]);

    useEffect(() => {
        setWaitData(data.filter(e => e.status === "Status.TODO"));
        setDoneData(data.filter(e => e.status === "Status.DONE"));
    }, [data]);

    return (
        <List
            component="nav"
            aria-labelledby="nested-list-subheader"
            className={classes.root}
        >
            <ListItem button component={props => <Link to="/upload" {...props} />}>
                <ListItemIcon>
                    <PublishIcon/>
                </ListItemIcon>
                <ListItemText primary="Upload"/>
            </ListItem>
            <ExpandList
                icon={<DraftsIcon/>}
                title="Waiting"
                data={waitData}
                positionIcon={<StarHalf/>}
            />
            <ExpandList
                icon={<InboxIcon/>}
                title="Done"
                data={doneData}
                positionIcon={<Star/>}
            />
        </List>
    );
};