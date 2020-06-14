import React, {StyleSheet, Dimensions, PixelRatio} from "react-native";
const {width, height, scale} = Dimensions.get("window"),
    vw = width / 100,
    vh = height / 100,
    vmin = Math.min(vw, vh),
    vmax = Math.max(vw, vh);

export default StyleSheet.create({
    "html": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none"
    },
    "head": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none"
    },
    "body": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none",
        "background": "#fff",
        "fontFamily": "'open_sansregular'",
        "fontSize": 13,
        "color": "#1c1c1e"
    },
    "p": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none",
        "textAlign": "justify"
    },
    "a": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none",
        "textDecoration": "none"
    },
    "h1": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none",
        "fontFamily": "'open_sansbold'"
    },
    "h2": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none",
        "fontFamily": "'open_sansbold'"
    },
    "h3": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none",
        "fontFamily": "'open_sansbold'"
    },
    "h4": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none"
    },
    "h5": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none"
    },
    "h6": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none"
    },
    "div": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none"
    },
    "img": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none",
        "maxWidth": "100%"
    },
    "ul": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none",
        "listStyle": "none"
    },
    "li": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none",
        "listStyle": "none"
    },
    "ol": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "outline": "none",
        "border": "none"
    },
    "button": {
        "outline": "#95C809"
    },
    "a:hover": {
        "textDecoration": "none"
    },
    "m_top02": {
        "marginTop": 2
    },
    "m_top05": {
        "marginTop": 5
    },
    "m_top08": {
        "marginTop": 8
    },
    "m_top10": {
        "marginTop": 10
    },
    "m_top20": {
        "marginTop": 20
    },
    "m_top25": {
        "marginTop": 25
    },
    "m_top30": {
        "marginTop": 30
    },
    "m_right03": {
        "marginRight": 3
    },
    "m_right05": {
        "marginRight": 5
    },
    "m_right08": {
        "marginRight": 8
    },
    "m_right10": {
        "marginRight": 10
    },
    "m_right15": {
        "marginRight": 15
    },
    "m_right20": {
        "marginRight": 20
    },
    "m_right30": {
        "marginRight": 30
    },
    "m_right50": {
        "marginRight": 50
    },
    "m_left05": {
        "marginLeft": 5
    },
    "m_left10": {
        "marginLeft": 10
    },
    "m_left20": {
        "marginLeft": 20
    },
    "m_left30": {
        "marginLeft": 30
    },
    "m_left40": {
        "marginLeft": 40
    },
    "m_bot05": {
        "marginBottom": 5
    },
    "m_bot08": {
        "marginBottom": 8
    },
    "m_bot10": {
        "marginBottom": 10
    },
    "m_bot15": {
        "marginBottom": 15
    },
    "m_bot20": {
        "marginBottom": 20
    },
    "m_bot25": {
        "marginBottom": 25
    },
    "m_bot30": {
        "marginBottom": 30
    },
    "p_top02": {
        "paddingTop": 2
    },
    "p_top05": {
        "paddingTop": 5
    },
    "p_top10": {
        "paddingTop": 10
    },
    "p_top15": {
        "paddingTop": 15
    },
    "p_top20": {
        "paddingTop": 20
    },
    "p_top25": {
        "paddingTop": 25
    },
    "p_top45": {
        "paddingTop": 45
    },
    "p_left05": {
        "paddingLeft": 5
    },
    "p_left10": {
        "paddingLeft": 10
    },
    "p_left15": {
        "paddingLeft": 15
    },
    "p_left20": {
        "paddingLeft": 20
    },
    "p_left30": {
        "paddingLeft": 30
    },
    "p_left35": {
        "paddingLeft": 35
    },
    "p_left70": {
        "paddingLeft": 70
    },
    "p_left110": {
        "paddingLeft": 110
    },
    "p_bot05": {
        "paddingBottom": 5
    },
    "p_bot08": {
        "paddingBottom": 8
    },
    "p_bot10": {
        "paddingBottom": 10
    },
    "p_bot15": {
        "paddingBottom": 15
    },
    "p_bot20": {
        "paddingBottom": 20
    },
    "p_bot30": {
        "paddingBottom": 30
    },
    "p_bot50": {
        "paddingBottom": 50
    },
    "p_rig05": {
        "paddingRight": 5
    },
    "p_rig10": {
        "paddingRight": 10
    },
    "p_rig15": {
        "paddingRight": 15
    },
    "p_rig20": {
        "paddingRight": 20
    },
    "p_rig25": {
        "paddingRight": 25
    },
    "p_rig30": {
        "paddingRight": 30
    },
    "left": {
        "float": "left"
    },
    "right": {
        "float": "right"
    },
    "header": {
        "background": "#fff",
        "paddingTop": 10,
        "paddingRight": 0,
        "paddingBottom": 10,
        "paddingLeft": 0
    },
    "search_s": {
        "position": "relative",
        "marginTop": 45
    },
    "submit": {
        "position": "absolute",
        "top": 0,
        "right": 0,
        "background": "#95c809",
        "width": "auto",
        "height": "auto",
        "border": "none",
        "fontFamily": "'open_sansbold'",
        "fontSize": 14,
        "color": "#ffffff",
        "textTransform": "uppercase",
        "textShadow": "0px 1px 1px rgba(149, 200, 9, 0.75)",
        "outline": "none",
        "paddingTop": 11,
        "paddingRight": 20,
        "paddingBottom": 11,
        "paddingLeft": 20
    },
    "btn-submit": {
        "background": "#95c809",
        "width": "auto",
        "height": "auto",
        "border": "none",
        "fontFamily": "'open_sansbold'",
        "fontSize": 14,
        "color": "#ffffff",
        "textTransform": "uppercase",
        "textShadow": "0px 1px 1px rgba(149, 200, 9, 0.75)",
        "outline": "none",
        "paddingTop": 11,
        "paddingRight": 20,
        "paddingBottom": 11,
        "paddingLeft": 20
    },
    "comm_input": {
        "height": 38,
        "paddingTop": 6,
        "paddingRight": 12,
        "paddingBottom": 6,
        "paddingLeft": 12,
        "border": "1px solid #e4e2e2",
        "borderRadius": 20,
        "fontSize": 13,
        "color": "#a6a6ac"
    },
    "comm_input:focus": {
        "borderColor": "#95c809",
        "outline": 0,
        "WebkitBoxShadow": "inset 0 1px 1px rgba(0, 0, 0, .075), 0 0 8px rgba(149, 200, 9, .6)",
        "boxShadow": "inset 0 1px 1px rgba(0, 0, 0, .075), 0 0 8px rgba(149, 200, 9, .6)"
    },
    "user_login_part": {
        "marginTop": 45
    },
    "user_pic": {
        "textAlign": "right",
        "paddingRight": 10,
        "display": "inline-block",
        "verticalAlign": "top"
    },
    "user_pic img": {
        "height": 35,
        "width": 35,
        "borderRadius": 100,
        "WebkitBorderRadius": 100,
        "MozBorderRadius": 100
    },
    "user_name_sec": {
        "textAlign": "left",
        "display": "inline-block"
    },
    "user_name_sec h3": {
        "fontFamily": "'open_sanssemibold'",
        "fontSize": 16
    },
    "nav": {
        "background": "#0b1c47 url(../images/nav_bg.jpg) repeat-x top center",
        "borderBottom": "6px solid #95c809"
    },
    "banner_n": {
        "background": "url(../images/banner_bg1.jpg) no-repeat top left"
    },
    "banner": {
        "background": "url(../images/banner_bg.jpg) no-repeat top left"
    },
    "banner_new_bg": {
        "background": "url(../images/banner_n_bg.png) repeat-x top left"
    },
    "banner_new_bg2": {
        "background": "#fff url(../images/banner_n_bg2.png) repeat-x top left"
    },
    "banner_fill": {
        "backgroundSize": "cover"
    },
    "inner_banner": {
        "marginTop": 68,
        "marginRight": 0,
        "marginBottom": 68,
        "marginLeft": 0,
        "background": "#fff",
        "paddingTop": 15,
        "paddingRight": 15,
        "paddingBottom": 15,
        "paddingLeft": 15,
        "zIndex": 99,
        "position": "relative",
        "WebkitBoxShadow": "0px 1px 5px 0px rgba(24, 27, 25, 0.32)",
        "MozBoxShadow": "0px 1px 5px 0px rgba(24, 27, 25, 0.32)",
        "boxShadow": "0px 1px 5px 0px rgba(24, 27, 25, 0.32)"
    },
    "inner_banner_2": {
        "paddingTop": 30,
        "paddingRight": 70,
        "paddingBottom": 5,
        "paddingLeft": 70
    },
    "heading_s": {
        "textAlign": "center"
    },
    "heading_s_left": {
        "textAlign": "left",
        "paddingTop": 8,
        "paddingRight": 0,
        "paddingBottom": 8,
        "paddingLeft": 0
    },
    "heading_s span": {
        "fontFamily": "'open_sansbold'",
        "fontSize": 22,
        "textTransform": "uppercase",
        "verticalAlign": "middle"
    },
    "banner_c": {
        "marginTop": 30,
        "marginRight": 0,
        "marginBottom": 20,
        "marginLeft": 0
    },
    "banner_c_search": {
        "marginTop": 30,
        "marginRight": 0,
        "marginBottom": 20,
        "marginLeft": 0
    },
    "right_txt": {
        "textAlign": "right"
    },
    "listing_ul li": {
        "fontSize": 15,
        "fontFamily": "'open_sanssemibold'",
        "marginBottom": 30,
        "width": "100%",
        "float": "left",
        "fontWeight": "500"
    },
    "listing_ul li span": {
        "fontSize": 16
    },
    "listing_ul li spanbold_txt": {
        "fontSize": 15,
        "fontFamily": "'open_sansbold'"
    },
    "listing_ul li ul li": {
        "float": "right",
        "textAlign": "right",
        "width": "auto",
        "paddingLeft": 5,
        "verticalAlign": "middle",
        "lineHeight": 32,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0
    },
    "f_nav": {
        "zIndex": 9999,
        "position": "fixed",
        "top": 0,
        "width": "100%"
    },
    "listing_ul_r li": {
        "fontSize": 15,
        "fontFamily": "'open_sanssemibold'",
        "marginBottom": 30,
        "width": "100%",
        "float": "left",
        "fontWeight": "500"
    },
    "listing_ul_r li span": {
        "fontSize": 16
    },
    "listing_ul_r li spanbold_txt": {
        "fontSize": 15,
        "fontFamily": "'open_sansbold'"
    },
    "listing_ul_r li ul li": {
        "float": "left",
        "textAlign": "right",
        "width": "auto",
        "paddingRight": 5,
        "verticalAlign": "middle",
        "lineHeight": 32,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0
    },
    "center_img": {
        "textAlign": "center"
    },
    "bottom": {
        "background": "#95C809",
        "paddingTop": 10,
        "paddingRight": 0,
        "paddingBottom": 10,
        "paddingLeft": 0
    },
    "popover": {
        "background": "#FFF",
        "paddingTop": 10,
        "paddingRight": 0,
        "paddingBottom": 10,
        "paddingLeft": 0,
        "maxWidth": "100%",
        "width": 500,
        "borderRadius": 0,
        "lineHeight": 30
    },
    "bottom_ul": {
        "textAlign": "center",
        "paddingTop": 0,
        "paddingRight": 15,
        "paddingBottom": 0,
        "paddingLeft": 15
    },
    "bottom_ul li": {
        "display": "inline-block",
        "paddingTop": 0,
        "paddingRight": 5,
        "paddingBottom": 0,
        "paddingLeft": 5
    },
    "bottom_ul li span": {
        "fontFamily": "'open_sanssemibold'",
        "color": "#fff"
    },
    "newsletter": {
        "position": "relative",
        "width": 320,
        "marginTop": 0,
        "marginRight": 20,
        "marginBottom": 0,
        "marginLeft": 20
    },
    "newsletter newslltr_input": {
        "background": "#fff",
        "height": 35,
        "width": "100%",
        "border": "none",
        "paddingTop": 3,
        "paddingRight": 10,
        "paddingBottom": 3,
        "paddingLeft": 10,
        "color": "#b2acac",
        "fontFamily": "'open_sanssemibold'",
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "borderRadius": 0,
        "display": "inline-block"
    },
    "newsletter submit_news": {
        "position": "absolute",
        "top": 0,
        "right": 0,
        "border": "none",
        "fontSize": 0,
        "background": "#00115e url(../images/email_icon.png) no-repeat scroll 50% 50%",
        "width": 47,
        "height": 35
    },
    "footer": {
        "background": "#00115e",
        "color": "#ffffff"
    },
    "footer h3": {
        "marginBottom": 20
    },
    "footer ul li": {
        "lineHeight": 24
    },
    "footer ul li a": {
        "color": "#fff"
    },
    "footer p": {
        "lineHeight": 22
    },
    "copyright": {
        "background": "#010e46",
        "paddingTop": 10,
        "paddingRight": 0,
        "paddingBottom": 10,
        "paddingLeft": 0,
        "color": "#ffffff",
        "fontSize": 12
    },
    "copyright_ul li": {
        "display": "inline-block",
        "paddingTop": 0,
        "paddingRight": 0.3,
        "paddingBottom": 0,
        "paddingLeft": 0.3,
        "fontSize": 12
    },
    "copyright_ul li a": {
        "color": "#fff"
    },
    "copyright_ul li a:hover": {
        "color": "#95c809"
    },
    "facebook": {
        "background": "url(../images/facebook.png) no-repeat top center",
        "border": "1px solid transparent",
        "borderRadius": 100
    },
    "facebook:hover": {
        "background": "url(../images/facebook_hover.png) no-repeat top center",
        "border": "1px solid #fff"
    },
    "twitter": {
        "background": "url(../images/twitter.png) no-repeat top center",
        "border": "1px solid transparent",
        "borderRadius": 100
    },
    "twitter:hover": {
        "background": "url(../images/twitter_hover.png) no-repeat top center",
        "border": "1px solid #fff"
    },
    "youtube": {
        "background": "url(../images/youtube.png) no-repeat top center",
        "border": "1px solid transparent",
        "borderRadius": 100
    },
    "youtube:hover": {
        "background": "url(../images/youtube_hover.png) no-repeat top center",
        "border": "1px solid #fff"
    },
    "linkedin": {
        "background": "url(../images/linkedin.png) no-repeat top center",
        "border": "1px solid transparent",
        "borderRadius": 100
    },
    "linkedin:hover": {
        "background": "url(../images/linkedin_hover.png) no-repeat top center",
        "border": "1px solid #fff"
    },
    "google_plus": {
        "background": "url(../images/google_plus.png) no-repeat top center",
        "border": "1px solid transparent",
        "borderRadius": 100
    },
    "google_plus:hover": {
        "background": "url(../images/google_plus_hover.png) no-repeat top center",
        "border": "1px solid #fff"
    },
    "icons_h": {
        "width": 31,
        "height": 31,
        "fontSize": 0,
        "display": "inline-block",
        "borderRadius": "50%",
        "verticalAlign": "middle",
        "WebkitTransition": "all ease 0.3s",
        "MozTransition": "all ease 0.3s",
        "OTransition": "all ease 0.3s",
        "MsTransition": "all ease 0.3s",
        "transition": "all ease 0.3s"
    },
    "icons_h:hover": {
        "boxShadow": "0px 0px 4px 1px rgba(0, 0, 0, 0.2)",
        "WebkitTransform": "rotate(360deg)",
        "MozTransform": "rotate(360deg)",
        "OTransform": "rotate(360deg)",
        "MsTransform": "rotate(360deg)",
        "transform": "rotate(360deg)"
    },
    "main_cont": {
        "paddingTop": 20,
        "paddingRight": 0,
        "paddingBottom": 20,
        "paddingLeft": 0
    },
    "profile_left": {
        "paddingTop": 15,
        "paddingRight": 15,
        "paddingBottom": 15,
        "paddingLeft": 15,
        "backgroundColor": "#FFFFFF",
        "border": "1px solid #e3e1e1"
    },
    "profile_right": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0
    },
    "profile_right h1": {
        "paddingTop": 15,
        "paddingRight": 15,
        "paddingBottom": 15,
        "paddingLeft": 15,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0
    },
    "right_p_bg": {
        "background": "#f5f8f9",
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "borderTop": "1px solid #e4e2e2",
        "borderBottom": "1px solid #e4e2e2",
        "WebkitBoxShadow": "inset 4px 0px 10px -1px rgba(220, 225, 227, 0.75)",
        "MozBoxShadow": "inset 4px 0px 10px -1px rgba(220, 225, 227, 0.75)",
        "boxShadow": "inset 4px 0px 10px -1px rgba(220, 225, 227, 0.75)"
    },
    "right_p_bg ul li": {
        "paddingTop": 10,
        "paddingRight": 15,
        "paddingBottom": 10,
        "paddingLeft": 15,
        "borderBottom": "1px solid #e4e2e2",
        "width": "100%",
        "lineHeight": 16,
        "verticalAlign": "middle",
        "display": "inline-flex",
        "WebkitBoxPack": "center",
        "MozBoxPack": "center",
        "MsFlexPack": "center",
        "MsFlexAlign": "center",
        "WebkitAlignItems": "center",
        "alignItems": "center",
        "WebkitBoxOrient": "vertical",
        "MozBoxOrient": "vertical"
    },
    "right_p_bg ul li:last-child": {
        "borderBottom": "none"
    },
    "right_p_bg ul li:hover": {
        "cursor": "pointer",
        "WebkitBoxShadow": "inset 0px 6px 10px 0px rgba(220, 225, 227, 0.75)",
        "MozBoxShadow": "inset 0px 6px 10px 0px rgba(220, 225, 227, 0.75)",
        "boxShadow": "inset 0px 6px 10px 0px rgba(220, 225, 227, 0.75)"
    },
    "clear-hover-li:hover": {
        "WebkitBoxShadow": "none !important",
        "MozBoxShadow": "none !important",
        "boxShadow": "none !important"
    },
    "profile_right h2": {
        "paddingTop": 15,
        "paddingRight": 15,
        "paddingBottom": 15,
        "paddingLeft": 15,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0
    },
    "text-center": {
        "textAlign": "center"
    },
    "right_p_bg2": {
        "background": "#f5f8f9",
        "paddingTop": 20,
        "paddingRight": 15,
        "paddingBottom": 20,
        "paddingLeft": 15,
        "borderTop": "1px solid #e4e2e2",
        "borderBottom": "1px solid #e4e2e2",
        "WebkitBoxShadow": "inset 4px 0px 10px -1px rgba(220, 225, 227, 0.75)",
        "MozBoxShadow": "inset 4px 0px 10px -1px rgba(220, 225, 227, 0.75)",
        "boxShadow": "inset 4px 0px 10px -1px rgba(220, 225, 227, 0.75)",
        "textAlign": "center"
    },
    "semibold_txt": {
        "fontFamily": "'open_sanssemibold'"
    },
    "semibold_txt span": {
        "fontFamily": "'open_sansbold'",
        "textTransform": "uppercase"
    },
    "buttn": {
        "fontFamily": "'open_sansbold'",
        "border": "1px solid #eee9e9",
        "marginTop": 20,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "display": "inline-block",
        "paddingTop": 10,
        "paddingRight": 0,
        "paddingBottom": 10,
        "paddingLeft": 0,
        "background": "#ffffff",
        "width": 180,
        "textAlign": "center"
    },
    "buttn1": {
        "fontFamily": "'open_sansbold'",
        "border": "1px solid #eee9e9",
        "display": "inline-block",
        "paddingTop": 10,
        "paddingRight": 35,
        "paddingBottom": 10,
        "paddingLeft": 35,
        "background": "#ffffff",
        "textAlign": "center"
    },
    "buttn2": {
        "fontFamily": "'open_sansbold'",
        "border": "1px solid #eee9e9",
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "display": "inline-block",
        "paddingTop": 10,
        "paddingRight": 0,
        "paddingBottom": 10,
        "paddingLeft": 0,
        "background": "#ffffff",
        "width": "100%",
        "textAlign": "center"
    },
    "buttn3": {
        "fontFamily": "'open_sansbold'",
        "border": 0,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "display": "inline-block",
        "background": "#ffffff",
        "textAlign": "center",
        "paddingTop": 2,
        "paddingRight": 10,
        "paddingBottom": 2,
        "paddingLeft": 10,
        "color": "#989890",
        "fontWeight": "400"
    },
    "buttn3:hover": {
        "color": "rgba(0, 0, 0, 0.5)"
    },
    "buttn_left": {
        "fontFamily": "'open_sansbold'",
        "border": "1px solid #eee9e9",
        "marginTop": 20,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "display": "inline-block",
        "paddingTop": 10,
        "paddingRight": 0,
        "paddingBottom": 10,
        "paddingLeft": 0,
        "background": "#ffffff",
        "width": "100%",
        "textAlign": "center"
    },
    "right_p_bg3": {
        "background": "#f5f8f9",
        "paddingTop": 20,
        "paddingRight": 15,
        "paddingBottom": 20,
        "paddingLeft": 15,
        "borderTop": "1px solid #e4e2e2",
        "borderBottom": "none",
        "WebkitBoxShadow": "inset 4px 0px 10px -1px rgba(220, 225, 227, 0.75)",
        "MozBoxShadow": "inset 4px 0px 10px -1px rgba(220, 225, 227, 0.75)",
        "boxShadow": "inset 4px 0px 10px -1px rgba(220, 225, 227, 0.75)"
    },
    "right_p_bg3 ul li": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "float": "left",
        "width": "80%"
    },
    "right_p_bg3 ul li:first-child": {
        "width": "20%"
    },
    "right_p_bg3 ul li img": {
        "borderRadius": "50%",
        "width": 40,
        "height": 40
    },
    "gap": {
        "height": 94
    },
    "gap2": {
        "height": 65
    },
    "gap3": {
        "height": 55
    },
    "right_p_bg2 ul li": {
        "display": "inline-block"
    },
    "bg_colr": {
        "background": "#fff",
        "border": "1px solid #e3e1e1",
        "position": "relative"
    },
    "seperate_line": {
        "position": "absolute",
        "borderRight": "1px solid #e3e1e1",
        "left": "75%",
        "height": "100%",
        "width": 1
    },
    "small_txt": {
        "fontSize": 12
    },
    "delete_link": {
        "color": "#00125f"
    },
    "rank_secs": {
        "paddingTop": 20,
        "paddingRight": 0,
        "paddingBottom": 20,
        "paddingLeft": 0,
        "position": "relative"
    },
    "rank_secs h1": {
        "borderBottom": "1px solid #ddd",
        "paddingBottom": 5
    },
    "rank_secs h1 span": {
        "fontSize": 12,
        "fontFamily": "'open_sansregular'"
    },
    "rank_details": {
        "marginLeft": -27,
        "marginTop": 20
    },
    "rank_details li": {
        "paddingBottom": 10,
        "background": "url(../images/small_bullet.png) no-repeat scroll 6px 16px",
        "paddingLeft": 35
    },
    "rank_details li span": {
        "paddingLeft": 5,
        "lineHeight": 40,
        "verticalAlign": "middle"
    },
    "rank_details liselected": {
        "background": "url(../images/big_bullet.png) no-repeat scroll 0 10px",
        "fontFamily": "'open_sansbold'"
    },
    "bold_txt": {
        "fontFamily": "'open_sansbold'"
    },
    "edit_txt": {
        "borderBottom": "1px solid #e6e8e9",
        "paddingBottom": 5,
        "marginTop": 20,
        "marginBottom": 10
    },
    "edit_txt i": {
        "color": "#dbd8d8",
        "fontSize": 16
    },
    "edit_txt a:hover i": {
        "color": "#95c809",
        "cursor": "pointer"
    },
    "personaldetails_list span": {
        "fontFamily": "'open_sansbold'"
    },
    "personaldetails_list li": {
        "paddingBottom": 10
    },
    "personaldetails_list i": {
        "color": "#dbd8d8",
        "fontSize": 16,
        "width": 30
    },
    "border_bot": {
        "borderBottom": "1px solid #e6e8e9",
        "paddingBottom": 10,
        "marginTop": 10,
        "marginRight": 0,
        "marginBottom": 10,
        "marginLeft": 0
    },
    "statis_ul li": {
        "marginBottom": 3,
        "float": "left",
        "width": "100%"
    },
    "statis_ul li i": {
        "background": "#f5f8f9",
        "paddingTop": 5,
        "paddingRight": 0,
        "paddingBottom": 5,
        "paddingLeft": 0,
        "width": "5%",
        "marginRight": "2%",
        "textAlign": "center",
        "float": "left"
    },
    "statis_ul li span": {
        "background": "#f5f8f9",
        "paddingTop": 5,
        "paddingRight": 5,
        "paddingBottom": 5,
        "paddingLeft": 5,
        "float": "left",
        "width": "93%"
    },
    "disabled_t": {
        "opacity": 0.3
    },
    "achievements_secs p": {
        "marginBottom": 10
    },
    "achievements_secs p img": {
        "marginRight": 5
    },
    "forum_post_list": {
        "background": "#f5f8f9",
        "paddingTop": 15,
        "paddingRight": 15,
        "paddingBottom": 15,
        "paddingLeft": 15,
        "marginBottom": 5
    },
    "tyml_txt": {
        "fontSize": 15,
        "color": "#8c8c8c"
    },
    "forum_post_list ul li": {
        "float": "left",
        "width": "90%"
    },
    "forum_post_list ul li img": {
        "border": "3px solid #fff"
    },
    "forum_post_list ul li:first-child": {
        "marginRight": "2%",
        "width": "8%"
    },
    "forum_post_list ul li p": {
        "paddingBottom": 5
    },
    "con_banner": {
        "background": "url(../images/banner_bg_new.jpg) no-repeat top left"
    },
    "achievements_ul li": {
        "minHeight": 35,
        "paddingLeft": 40,
        "paddingTop": 7,
        "marginBottom": 10
    },
    "images_secs": {
        "marginTop": 0,
        "position": "relative",
        "width": "100%",
        "display": "inline-block",
        "paddingTop": 0,
        "paddingRight": 205,
        "paddingBottom": 0,
        "paddingLeft": 205
    },
    "images_secs img": {
        "position": "absolute",
        "top": 20,
        "zIndex": 9,
        "left": 35
    },
    "inner_con_banner": {
        "marginTop": 365,
        "marginRight": "auto",
        "marginBottom": 60,
        "marginLeft": "auto",
        "background": "#fff",
        "paddingTop": 15,
        "paddingRight": 15,
        "paddingBottom": 15,
        "paddingLeft": 15,
        "zIndex": 99,
        "position": "relative",
        "minHeight": 333,
        "WebkitBoxShadow": "0px 1px 5px 0px rgba(24, 27, 25, 0.32)",
        "MozBoxShadow": "0px 1px 5px 0px rgba(24, 27, 25, 0.32)",
        "boxShadow": "0px 1px 5px 0px rgba(24, 27, 25, 0.32)",
        "width": "100%"
    },
    "main_cons": {
        "marginBottom": 30
    },
    "green_border_txt": {
        "borderBottom": "3px solid #8ec308",
        "paddingBottom": 7,
        "marginTop": 20,
        "marginBottom": 10,
        "position": "relative",
        "paddingRight": 20
    },
    "green_border_txt a": {
        "position": "absolute",
        "right": 0,
        "bottom": 4
    },
    "green_border_txt i": {
        "color": "#dad7d7",
        "fontSize": 20
    },
    "green_border_txt a:hover i": {
        "color": "#8ec308"
    },
    "blue_s": {
        "background": "#f5f8f9",
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 5,
        "marginLeft": 0
    },
    "blue_s ul lihdng_typ1": {
        "background": "url(../images/aa.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ2": {
        "background": "url(../images/gg.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ3": {
        "background": "url(../images/gg2.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ4": {
        "background": "url(../images/aa.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ5": {
        "background": "url(../images/aa.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ6": {
        "background": "url(../images/gg.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ7": {
        "background": "url(../images/gg2.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ8": {
        "background": "url(../images/aa.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ9": {
        "background": "url(../images/aa.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ10": {
        "background": "url(../images/gg.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ11": {
        "background": "url(../images/gg2.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ12": {
        "background": "url(../images/aa.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ13": {
        "background": "url(../images/aa.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ14": {
        "background": "url(../images/gg.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ15": {
        "background": "url(../images/gg2.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul lihdng_typ16": {
        "background": "url(../images/aa.png) no-repeat top left",
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "blue_s ul li": {
        "display": "inline-block",
        "verticalAlign": "middle"
    },
    "blue_s ul li p": {
        "lineHeight": 20
    },
    "blue_s ul li psemibold_txt span": {
        "color": "#011460"
    },
    "pagin_ul": {
        "marginTop": 20
    },
    "pagin_ul li": {
        "display": "inline-block",
        "verticalAlign": "middle",
        "border": "1px solid #eee8e8",
        "paddingTop": 3,
        "paddingRight": "0.5%",
        "paddingBottom": 3,
        "paddingLeft": "0.5%",
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "float": "left",
        "borderRight": "none",
        "background": "#fcfcfc"
    },
    "pagin_ul li p": {
        "marginRight": 15
    },
    "pagin_ul li ul li": {
        "border": "1px solid #eee8e8",
        "paddingTop": 3,
        "paddingRight": 10,
        "paddingBottom": 3,
        "paddingLeft": 10,
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "float": "left",
        "borderRight": "none",
        "background": "#fcfcfc"
    },
    "pagin_ul li ul li:last-child": {
        "borderRight": "1px solid #eee8e8"
    },
    "pagin_ul li ul liactive": {
        "background": "#011460"
    },
    "pagin_ul li ul li:hover": {
        "background": "#011460"
    },
    "pagin_ul li ul liactive a": {
        "color": "#fff"
    },
    "pagin_ul li ul li:hover a": {
        "color": "#fff"
    },
    "spancustomSelect": {
        "fontSize": 11,
        "backgroundColor": "#fff",
        "color": "#7c7c7c",
        "paddingTop": 5,
        "paddingRight": 7,
        "paddingBottom": 5,
        "paddingLeft": 7,
        "border": "1px solid #eee8e8"
    },
    "spancustomSelectchanged": {
        "backgroundColor": "#f0dea4"
    },
    "customSelectInner": {
        "background": "url(../images/arrow.png) no-repeat center right",
        "paddingRight": 10,
        "minWidth": "90px !important"
    },
    "line_hgt": {
        "lineHeight": 28
    },
    "risk_secs risk_ul li": {
        "display": "block",
        "fontFamily": "'open_sanssemibold'"
    },
    "risk_secs risk_ul li ul li": {
        "display": "inline-block",
        "verticalAlign": "middle",
        "width": "78%",
        "paddingTop": 3,
        "paddingRight": 5,
        "paddingBottom": 3,
        "paddingLeft": 5
    },
    "risk_secs risk_ul li ul li:first-child": {
        "width": "20%"
    },
    "risk_secs risk_ul li:nth-child(2n)": {
        "background": "#f5f8f9"
    },
    "risk_secs risk_ul li ul li:nth-child(2n)": {
        "background": "transparent"
    },
    "right_contntpg": {
        "border": "1px solid #e4e2e2"
    },
    "right_contntpg h1": {
        "fontSize": 22,
        "background": "#95c809 url(../images/right_green_bg.jpg) no-repeat top left",
        "height": 45,
        "color": "#fff",
        "lineHeight": 45,
        "verticalAlign": "middle",
        "paddingLeft": 15
    },
    "right_contntpg ul li": {
        "background": "#f5f8f9",
        "paddingTop": 10,
        "paddingRight": 15,
        "paddingBottom": 10,
        "paddingLeft": 15,
        "borderTop": "1px solid #e4e2e2",
        "borderBottom": "none",
        "fontFamily": "'open_sanssemibold'",
        "WebkitBoxShadow": "inset 4px 0px 10px -1px rgba(220, 225, 227, 0.75)",
        "MozBoxShadow": "inset 4px 0px 10px -1px rgba(220, 225, 227, 0.75)",
        "boxShadow": "inset 4px 0px 10px -1px rgba(220, 225, 227, 0.75)"
    },
    "right_contntpg ul li span": {
        "color": "#011460"
    },
    "percentg_bar": {
        "width": "100%",
        "display": "inline-block"
    },
    "percentg_box": {
        "float": "left"
    },
    "percentg_bar per_1": {
        "width": "10%",
        "height": 13
    },
    "percentg_bar per_2": {
        "width": "100%",
        "height": 13
    },
    "percentg_bar per_3": {
        "width": "100%",
        "height": 13
    },
    "percentg_bar per_4": {
        "width": "100%",
        "height": 13
    },
    "percentg_bar per_5": {
        "width": "100%",
        "height": 13
    },
    "percentg_bar per_6": {
        "width": "100%",
        "height": 13
    },
    "percentg_bar per_7": {
        "width": "100%",
        "height": 13
    },
    "percentg_bar per_8": {
        "width": "100%",
        "height": 13
    },
    "percentg_bar per_9": {
        "width": "100%",
        "height": 13
    },
    "green_bg": {
        "background": "#95c809"
    },
    "blue_bg": {
        "background": "#011460"
    },
    "sky_bg": {
        "background": "#00b0f0"
    },
    "percentg_secs": {
        "paddingTop": 10,
        "paddingRight": 0,
        "paddingBottom": 10,
        "paddingLeft": 0,
        "minHeight": 100,
        "position": "relative"
    },
    "percentg_secspercent-type-0": {
        "display": "none"
    },
    "percentg_secs tooltip-bar": {
        "position": "relative"
    },
    "percentg_secspercent-type-3 tooltip-bar gennotype_wrapper:nth-child(2)": {
        "position": "absolute",
        "width": "100%",
        "top": 0,
        "left": 0,
        "paddingLeft": 63,
        "paddingRight": 63,
        "display": "block !important"
    },
    "tooltip_s": {
        "fontFamily": "'open_sanssemibold'",
        "marginTop": 3,
        "paddingTop": 5,
        "paddingRight": 1,
        "paddingBottom": 5,
        "paddingLeft": 1,
        "display": "block",
        "fontSize": 12,
        "fontWeight": "400",
        "lineHeight": 1.4,
        "opacity": 1,
        "position": "relative",
        "visibility": "visible",
        "float": "left",
        "zIndex": 13,
        "width": 63
    },
    "gennotype_wrapper:last-child tooltip_s": {
        "float": "right"
    },
    "gennotype_wrapper:first-child tooltip_s genotype-arrow-color": {
        "borderStyle": "solid",
        "height": 0,
        "width": 0,
        "borderColor": "transparent",
        "borderBottomColor": "#000",
        "borderWidth": "0 5px 12px",
        "left": "3%",
        "top": -4,
        "position": "absolute"
    },
    "gennotype_wrapper:nth-child(2) tooltip_s genotype-arrow-color": {
        "borderStyle": "solid",
        "height": 0,
        "width": 0,
        "borderColor": "transparent",
        "borderBottomColor": "#000",
        "borderWidth": "0 5px 12px",
        "left": "42%",
        "top": -4,
        "position": "absolute"
    },
    "gennotype_wrapper:last-child tooltip_s genotype-arrow-color": {
        "borderStyle": "solid",
        "height": 0,
        "width": 0,
        "borderColor": "transparent",
        "borderBottomColor": "#000",
        "borderWidth": "0 5px 12px",
        "right": "2%",
        "left": "inherit",
        "top": -4,
        "position": "absolute"
    },
    "tooltip_s tooltip_s_arrow-4": {
        "borderStyle": "solid",
        "height": 0,
        "width": 0,
        "borderColor": "transparent",
        "borderBottomColor": "#000",
        "borderWidth": "0 5px 12px",
        "right": "2%",
        "top": -4,
        "position": "absolute"
    },
    "div[id^=\"genotype-modal\"] modal-dialog": {
        "maxWidth": 500
    },
    "tooltip_s_inner": {
        "backgroundColor": "#000",
        "borderRadius": 4,
        "color": "#fff",
        "maxWidth": 200,
        "paddingTop": 6,
        "paddingRight": 10,
        "paddingBottom": 6,
        "paddingLeft": 10,
        "textAlign": "center",
        "textDecoration": "none",
        "WebkitBoxShadow": "0px 1px 5px 0px rgba(24, 27, 25, 0.32)",
        "MozBoxShadow": "0px 2px 5px 0px rgba(24, 27, 25, 0.32)",
        "boxShadow": "0px 2px 5px 0px rgba(24, 27, 25, 0.32)"
    },
    "tooltip_s_inner span": {
        "fontFamily": "'open_sansbold'"
    },
    "tooltip_sblue tooltip_s_inner": {
        "background": "#011460"
    },
    "tooltip_ssky tooltip_s_inner": {
        "background": "#00b0f0"
    },
    "tooltip_sgreen tooltip_s_inner": {
        "background": "#95c809"
    },
    "tooltip_sblue tooltip_s_arrow": {
        "borderBottomColor": "#011460"
    },
    "tooltip_ssky tooltip_s_arrow": {
        "borderBottomColor": "#00b0f0"
    },
    "tooltip_sgreen tooltip_s_arrow": {
        "borderBottomColor": "#95c809"
    },
    "left_3": {
        "left": "25%"
    },
    "left_5": {
        "left": "35%"
    },
    "left_7": {
        "left": "75%"
    },
    "commnt_box": {
        "border": "1px solid #e3e0e0",
        "paddingTop": 15,
        "paddingRight": 15,
        "paddingBottom": 15,
        "paddingLeft": 15,
        "marginTop": 20,
        "marginRight": 0,
        "marginBottom": 20,
        "marginLeft": 0
    },
    "commnt_box_ul": {
        "paddingTop": 10,
        "paddingRight": 0,
        "paddingBottom": 10,
        "paddingLeft": 0,
        "marginTop": 10
    },
    "commnt_box_ul li": {
        "display": "inline-block",
        "width": "89%",
        "verticalAlign": "top",
        "position": "relative"
    },
    "commnt_box_ul li:first-child": {
        "width": "10%",
        "paddingRight": 5
    },
    "commnt_box_ul textareaform-control": {
        "resize": "none",
        "borderRadius": 0
    },
    "pos_img": {
        "position": "absolute",
        "left": -9,
        "top": 10
    },
    "commnt_box_ul p": {
        "lineHeight": 22
    },
    "commnt_box_ul span": {
        "color": "#858587",
        "fontSize": 12,
        "fontFamily": "'open_sansregular'",
        "marginLeft": 10
    },
    "smll_pag_ul": {
        "marginTop": 15
    },
    "smll_pag_ul li:first-child": {
        "width": "auto"
    },
    "smll_pag_ul li": {
        "display": "inline-block",
        "verticalAlign": "middle",
        "width": "auto",
        "paddingRight": 10
    },
    "smll_pag_ul li a i": {
        "color": "#cecece"
    },
    "smll_pag_ul li a:hover i": {
        "color": "#95c809"
    },
    "blue": {
        "color": "#01114F"
    },
    "commnt_secs": {
        "paddingTop": 0,
        "paddingRight": 210,
        "paddingBottom": 0,
        "paddingLeft": 210,
        "marginBottom": 30
    },
    "left_contnt_secs": {
        "paddingLeft": 210,
        "width": "63%",
        "float": "left"
    },
    "devide_secs": {
        "marginTop": 30,
        "paddingRight": 210,
        "float": "right",
        "width": "35%",
        "position": "relative"
    },
    "devide_secs h1": {
        "fontSize": 18
    },
    "seperate_line_inbox": {
        "position": "absolute",
        "borderRight": "1px solid #e3e1e1",
        "left": "25%",
        "height": "100%",
        "width": 1
    },
    "heading_p": {
        "textAlign": "center"
    },
    "search_heading": {
        "background": "url(../images/heading_bg.png) no-repeat top left",
        "height": 53,
        "lineHeight": 53,
        "verticalAlign": "middle",
        "paddingLeft": 110
    },
    "search_ul li": {
        "paddingLeft": 110,
        "fontFamily": "'open_sanssemibold'",
        "lineHeight": 24
    },
    "search_heading_right": {
        "background": "url(../images/heading_bg.png) no-repeat top left",
        "height": 53,
        "lineHeight": 53,
        "verticalAlign": "middle",
        "paddingLeft": 60
    },
    "search_ul_right li": {
        "paddingLeft": 60,
        "fontFamily": "'open_sanssemibold'",
        "lineHeight": 24
    },
    "search_input": {
        "position": "relative"
    },
    "search_input absolute_i": {
        "position": "absolute",
        "top": 10,
        "left": 10
    },
    "search_input input_a": {
        "paddingLeft": 30,
        "borderRadius": 0,
        "border": "none"
    },
    "user_s": {
        "position": "relative",
        "width": "18%",
        "float": "left",
        "marginRight": "2%",
        "textAlign": "center"
    },
    "user_s img": {
        "borderRadius": 100,
        "MozBorderRadius": 100,
        "WebkitBorderRadius": 100,
        "height": 40,
        "width": 40
    },
    "user_s span": {
        "position": "absolute",
        "right": 0,
        "bottom": 0,
        "borderRadius": 100,
        "MozBorderRadius": 100,
        "WebkitBorderRadius": 100,
        "height": 20,
        "width": 20,
        "background": "#95c809",
        "color": "#fff",
        "textAlign": "center",
        "fontFamily": "'open_sansextrabold'",
        "fontSize": 10
    },
    "vert_mid": {
        "lineHeight": 16,
        "verticalAlign": "middle",
        "display": "inline-flex",
        "WebkitBoxPack": "center",
        "MozBoxPack": "center",
        "MsFlexPack": "center",
        "WebkitJustifyContent": "center",
        "justifyContent": "center",
        "MsFlexAlign": "center",
        "WebkitAlignItems": "center",
        "alignItems": "center",
        "WebkitBoxOrient": "vertical",
        "MozBoxOrient": "vertical"
    },
    "user_name_r": {
        "width": "79%",
        "float": "right",
        "lineHeight": 40
    },
    "inbox_right": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0
    },
    "inbox_border": {
        "borderBottom": "1px solid #e5e2e2",
        "paddingTop": 15,
        "paddingRight": 15,
        "paddingBottom": 15,
        "paddingLeft": 15
    },
    "round_img": {
        "width": 40,
        "height": 40,
        "borderRadius": "50%",
        "WebkitBorderRadius": "50%",
        "MozBorderRadius": "50%"
    },
    "post_img": {
        "marginTop": 20,
        "marginRight": 0,
        "marginBottom": 20,
        "marginLeft": 0,
        "border": "1px solid #e5e2e2"
    },
    "commnt_post_secs": {
        "background": "#f5f8f9",
        "paddingTop": 15,
        "paddingRight": 15,
        "paddingBottom": 15,
        "paddingLeft": 15,
        "border": "1px solid #d1d8d5",
        "borderRight": "none"
    },
    "p_cmnt_s": {
        "background": "#fff",
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0,
        "border": "1px solid #d1d8d5"
    },
    "post_elemnt": {},
    "post_elemnt ul li": {
        "display": "inline-block",
        "verticalAlign": "middle",
        "paddingTop": 5,
        "paddingRight": 0,
        "paddingBottom": 5,
        "paddingLeft": 15
    },
    "post_elemnt ul li a:hover i": {
        "color": "#95c809"
    },
    "post_elemnt ul li i": {
        "color": "#c8c6c6",
        "fontSize": 18
    },
    "post_elemnt ul li:last-child": {
        "paddingTop": 0,
        "paddingRight": 0,
        "paddingBottom": 0,
        "paddingLeft": 0
    },
    "trans_textarea": {
        "border": "none",
        "resize": "none",
        "paddingTop": 15,
        "paddingRight": 15,
        "paddingBottom": 15,
        "paddingLeft": 15,
        "width": "100%"
    },
    "transform": {
        "WebkitTransform": "rotate(90deg)",
        "MozTransform": "rotate(90deg)",
        "MsTransform": "rotate(90deg)",
        "OTransform": "rotate(90deg)",
        "transform": "rotate(90deg)"
    },
    "reply_link": {
        "background": "#00115e",
        "paddingTop": 6,
        "paddingRight": 15,
        "paddingBottom": 6,
        "paddingLeft": 15,
        "color": "#fff",
        "display": "inline-block",
        "textTransform": "none",
        "fontFamily": "'open_sansbold'"
    },
    "search_s input-lg": {
        "fontSize": 13
    },
    "heading_p h1": {
        "paddingTop": 35,
        "paddingRight": 0,
        "paddingBottom": 35,
        "paddingLeft": 0
    },
    "link_bottom": {
        "border": "1px solid #ddd",
        "cursor": "pointer",
        "paddingTop": 3,
        "paddingRight": 18.5,
        "paddingBottom": 3,
        "paddingLeft": 18.5,
        "background": "#011460",
        "color": "#fff",
        "marginTop": 0,
        "height": 26
    },
    "copyright a": {
        "color": "#fff"
    },
    "devide_secs risk_secs risk_ul li ul li:first-child": {
        "width": "25%"
    },
    "devide_secs risk_ul li ul li": {
        "display": "inline-block",
        "paddingTop": 3,
        "paddingRight": 5,
        "paddingBottom": 3,
        "paddingLeft": 5,
        "verticalAlign": "middle",
        "width": "73%"
    },
    "containerinnerpart": {
        "paddingTop": 0,
        "paddingRight": 208,
        "paddingBottom": 0,
        "paddingLeft": 208,
        "minHeight": 500
    },
    "devide_secs1": {
        "marginTop": 2,
        "position": "relative"
    },
    "devide_secs1 h1": {
        "fontSize": 18
    },
    "innertable table": {
        "width": "100%"
    },
    "innertable th": {
        "paddingTop": 4,
        "paddingRight": 20,
        "paddingBottom": 4,
        "paddingLeft": 7,
        "verticalAlign": "top"
    },
    "innertable td": {
        "paddingTop": 4,
        "paddingRight": 20,
        "paddingBottom": 4,
        "paddingLeft": 7,
        "color": "#000",
        "textAlign": "left",
        "verticalAlign": "top"
    },
    "innertable table > thead > tr > th": {
        "borderBottom": "none !important"
    },
    "buttonviewGenotypecollapsed:before": {
        "content": "'View all'",
        "display": "block"
    },
    "buttonviewGenotype:before": {
        "content": "'View summary'",
        "display": "block"
    },
    "clickable": {
        "cursor": "pointer"
    },
    "clickable a:hover": {
        "textDecoration": "underline"
    },
    "genotype-arrow-color": {
        "borderBottomColor": "inherit !important"
    },
    "modal-content": {
        "WebkitBorderRadius": "0px !important",
        "MozBorderRadius": "0px !important",
        "borderRadius": "0px !important",
        "marginTop": 60
    },
    "genotype-header": {},
    "genotype-header p": {
        "paddingTop": 2
    },
    "genotype-header p > span": {
        "color": "#989890"
    },
    "population-name": {
        "fontSize": 15
    },
    "gennotype_color-1": {
        "background": "#011460"
    },
    "gennotype_color-2": {
        "background": "#00b0f0"
    },
    "gennotype_color-3": {
        "background": "#95c809"
    },
    "gennotype_color-4": {
        "background": "#F2B632"
    },
    "gennotype_border_color-1": {
        "borderColor": "#011460"
    },
    "gennotype_border_color-2": {
        "borderColor": "#00b0f0"
    },
    "gennotype_border_color-3": {
        "borderColor": "#95c809"
    },
    "gennotype_border_color-4": {
        "borderColor": "#F2B632"
    },
    "pagin_ul li:last-child": {
        "borderRight": "1px solid #eee8e8"
    },
    "pagin_ul liactive": {
        "background": "#011460"
    },
    "pagin_ul li:hover": {
        "background": "#011460"
    },
    "pagin_ul liactive a": {
        "color": "#fff"
    },
    "pagin_ul li:hover a": {
        "color": "#fff"
    },
    "about-cancel:hover i": {
        "color": "red !important",
        "cursor": "pointer"
    },
    "btn-blue": {
        "color": "#FFF",
        "background": "#01114F"
    },
    "btn-green": {
        "color": "#FFF",
        "background": "#95C809"
    },
    "green": {
        "color": "#95C809"
    },
    "listData_ul": {
        "width": "100%",
        "float": "left",
        "fontSize": 15,
        "fontWeight": "500"
    },
    "lilistData_ul_li": {
        "float": "left",
        "width": "50%",
        "paddingTop": 5,
        "paddingRight": 0,
        "paddingBottom": 5,
        "paddingLeft": 0
    },
    "listData_ul li a:hover": {
        "cursor": "pointer",
        "color": "#95c809"
    },
    "listData_ul li a": {
        "paddingTop": 0,
        "paddingRight": 5,
        "paddingBottom": 0,
        "paddingLeft": 5
    },
    "listData_ul li aassociated": {
        "color": "#95C809"
    },
    "ullist-letters": {
        "marginTop": 8,
        "marginRight": 0,
        "marginBottom": 16,
        "marginLeft": 0
    },
    "btn-pagi": {
        "backgroundColor": "#95c809",
        "color": "#ffffff",
        "borderRadius": 2,
        "marginTop": 0,
        "marginRight": 2,
        "marginBottom": 0,
        "marginLeft": 2
    },
    "btn-pagi:hover": {
        "backgroundColor": "#64DD17"
    },
    "pagination li span:hover": {
        "cursor": "pointer"
    },
    "pagination>li>a": {
        "border": "1px solid #F5F5F5",
        "color": "#1976D2"
    },
    "pagination>li>span": {
        "border": "1px solid #F5F5F5",
        "color": "#1976D2"
    },
    "buttn-hover-green:hover": {
        "background": "#95C809",
        "color": "#FFF"
    },
    "pop-emessage": {
        "fontWeight": "100",
        "fontSize": 12,
        "color": "red"
    },
    "gene-word": {
        "fontSize": 16,
        "color": "#011257",
        "fontFamily": "'open_sansregular'"
    },
    "bay-word": {
        "fontSize": 16,
        "color": "#95c809",
        "fontFamily": "'open_sansregular'",
        "paddingLeft": 2
    },
    "gb-white:hover > a > span": {
        "color": "#FFF"
    },
    "messActive": {},
    "messActive > div > a": {
        "color": "#95C809"
    },
    "btn-s-green": {
        "backgroundColor": "#95c809",
        "color": "#FFFFFF",
        "fontWeight": "bold",
        "paddingTop": 5,
        "paddingRight": 15,
        "paddingBottom": 5,
        "paddingLeft": 15
    },
    "btn-s-green:hover": {
        "backgroundColor": "#A4DC0A",
        "color": "#FFFFFF",
        "fontWeight": "bold",
        "paddingTop": 5,
        "paddingRight": 15,
        "paddingBottom": 5,
        "paddingLeft": 15
    },
    "btn-s-blue": {
        "backgroundColor": "#011257",
        "color": "#FFFFFF",
        "fontWeight": "bold",
        "paddingTop": 5,
        "paddingRight": 15,
        "paddingBottom": 5,
        "paddingLeft": 15
    },
    "btn-s-blue:hover": {
        "backgroundColor": "#01197A",
        "color": "#FFFFFF",
        "fontWeight": "bold",
        "paddingTop": 5,
        "paddingRight": 15,
        "paddingBottom": 5,
        "paddingLeft": 15
    },
    "sc-pmid": {
        "color": "#011258",
        "fontWeight": "500"
    },
    "sc-title": {
        "fontWeight": "bold",
        "fontSize": 13,
        "float": "left"
    },
    "sc-author": {
        "minHeight": 35
    },
    "sc-author span": {
        "float": "right",
        "fontSize": 12,
        "color": "#777782"
    },
    "sc-journal": {},
    "sc-journal p": {
        "fontSize": 12,
        "float": "right"
    },
    "sc-journal-id": {
        "paddingTop": 1,
        "paddingRight": 0,
        "paddingBottom": 1,
        "paddingLeft": 0,
        "float": "right"
    },
    "pub-right": {},
    "green-border-btm": {
        "borderBottom": "3px solid #8ec308"
    },
    "not-margin": {
        "marginTop": 0,
        "marginRight": 0,
        "marginBottom": 0,
        "marginLeft": 0
    },
    "body select2-container--default select2-selection": {
        "boxShadow": "2px 3px 2px #e8e8e8",
        "border": "1px solid #e4e2e2",
        "borderRadius": 0
    },
    "body select2-container--defaultselect2-container--focus select2-selection": {
        "boxShadow": "2px 3px 2px #e8e8e8",
        "border": "1px solid #e4e2e2",
        "borderRadius": 0
    },
    "select2-container": {
        "width": "100% !important"
    },
    "page-forum": {
        "overflowY": "hidden"
    },
    "form-grouprequired form-control": {
        "border": "1px solid red !important",
        "boxShadow": "none"
    },
    "form-grouprequired select2-selection": {
        "border": "1px solid red !important",
        "boxShadow": "none"
    },
    "holds-the-iframe": {
        "background": "url(../images/gif/loading-iframe.gif) center center no-repeat"
    },
    "tooltipbottom": {
        "background": "none !important"
    },
    "popover-content": {
        "maxHeight": 200,
        "overflowY": "scroll"
    },
    "dropdown-content": {
        "marginTop": "2px !important",
        "display": "none !important",
        "position": "fixed !important",
        "backgroundColor": "#f9f9f9 !important",
        "minWidth": "160px !important",
        "boxShadow": "0px 8px 16px 0px rgba(0,0,0,0.2) !important",
        "paddingTop": 12,
        "paddingRight": 16,
        "paddingBottom": "!important",
        "paddingLeft": 16,
        "zIndex": "1 !important"
    },
    "dropdown": {
        "position": "absolute !important"
    },
    "dropdown:hover dropdown-content": {
        "display": "inline !important"
    },
    "chro-1": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 126,
        "position": "absolute",
        "marginLeft": 5,
        "width": 55,
        "height": 139,
        "left": 303,
        "transform": "rotate(62deg)",
        "MsTransform": "rotate(62deg)",
        "WebkitTransform": "rotate(62deg)"
    },
    "transform-none-chro-1": {
        "transform": "rotate(-62deg)",
        "MsTransform": "rotate(-62deg)",
        "WebkitTransform": "rotate(-62deg)"
    },
    "chro-2": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 223,
        "position": "absolute",
        "marginLeft": 5,
        "width": 32,
        "height": 32,
        "left": 352
    },
    "chro-3": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 230,
        "position": "absolute",
        "marginLeft": 5,
        "width": 40,
        "height": 100,
        "left": 445,
        "transform": "rotate(44deg)",
        "MsTransform": "rotate(44deg)",
        "WebkitTransform": "rotate(44deg)"
    },
    "transform-none-chro-3": {
        "transform": "rotate(-44deg)",
        "MsTransform": "rotate(-44deg)",
        "WebkitTransform": "rotate(-44deg)"
    },
    "chro-4": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 220,
        "left": 526,
        "position": "absolute",
        "marginLeft": 5,
        "width": 25,
        "height": 60,
        "transform": "rotate(-35deg)",
        "MsTransform": "rotate(-35deg)",
        "WebkitTransform": "rotate(-35deg)"
    },
    "transform-none-chro-4": {
        "transform": "rotate(35deg)",
        "MsTransform": "rotate(35deg)",
        "WebkitTransform": "rotate(35deg)"
    },
    "chro-5": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 250,
        "left": 565,
        "position": "absolute",
        "marginLeft": 5,
        "width": 25,
        "height": 25
    },
    "chro-6": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 185,
        "left": 587,
        "position": "absolute",
        "marginLeft": 5,
        "width": 23,
        "height": 67,
        "transform": "rotate(-25deg)",
        "MsTransform": "rotate(-25deg)",
        "WebkitTransform": "rotate(-25deg)"
    },
    "transform-none-chro-6": {
        "transform": "rotate(25deg)",
        "MsTransform": "rotate(25deg)",
        "WebkitTransform": "rotate(25deg)"
    },
    "chro-7": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 230,
        "position": "absolute",
        "marginLeft": 5,
        "width": 25,
        "height": 50,
        "left": 666,
        "transform": "rotate(35deg)",
        "MsTransform": "rotate(35deg)",
        "WebkitTransform": "rotate(35deg)"
    },
    "transform-none-chro-7": {
        "transform": "rotate(-35deg)",
        "MsTransform": "rotate(-35deg)",
        "WebkitTransform": "rotate(-35deg)"
    },
    "chro-8": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 176,
        "left": 716,
        "position": "absolute",
        "marginLeft": 5,
        "width": 25,
        "height": 60,
        "transform": "rotate(55deg)",
        "MsTransform": "rotate(55deg)",
        "WebkitTransform": "rotate(55deg)"
    },
    "transform-none-chro-8": {
        "transform": "rotate(-55deg)",
        "MsTransform": "rotate(-55deg)",
        "WebkitTransform": "rotate(-55deg)"
    },
    "chro-9": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 248,
        "left": 712,
        "position": "absolute",
        "marginLeft": 5,
        "width": 20,
        "height": 32,
        "transform": "rotate(-40deg)",
        "MsTransform": "rotate(-40deg)",
        "WebkitTransform": "rotate(-40deg)"
    },
    "transform-none-chro-9": {
        "transform": "rotate(40deg)",
        "MsTransform": "rotate(40deg)",
        "WebkitTransform": "rotate(40deg)"
    },
    "chro-10": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 233,
        "left": 795,
        "position": "absolute",
        "marginLeft": -4,
        "width": 15,
        "height": 38,
        "transform": "rotate(-10deg)",
        "MsTransform": "rotate(-10deg)",
        "WebkitTransform": "rotate(-10deg)"
    },
    "transform-none-chro-10": {
        "transform": "rotate(10deg)",
        "MsTransform": "rotate(10deg)",
        "WebkitTransform": "rotate(10deg)"
    },
    "chro-11": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 170,
        "position": "absolute",
        "marginLeft": 5,
        "width": 15,
        "height": 65,
        "left": 845,
        "transform": "rotate(35deg)",
        "MsTransform": "rotate(35deg)",
        "WebkitTransform": "rotate(35deg)"
    },
    "transform-none-chro-11": {
        "transform": "rotate(-35deg)",
        "MsTransform": "rotate(-35deg)",
        "WebkitTransform": "rotate(-35deg)"
    },
    "chro-12": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 182,
        "left": 893,
        "position": "absolute",
        "marginLeft": 5,
        "width": 10,
        "height": 35,
        "transform": "rotate(-65deg)",
        "MsTransform": "rotate(-65deg)",
        "WebkitTransform": "rotate(-65deg)"
    },
    "transform-none-chro-12": {
        "transform": "rotate(65deg)",
        "MsTransform": "rotate(65deg)",
        "WebkitTransform": "rotate(65deg)"
    },
    "chro-13": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 175,
        "position": "absolute",
        "marginLeft": 5,
        "width": 12,
        "height": 46,
        "left": 813,
        "transform": "rotate(17deg)",
        "MsTransform": "rotate(17deg)",
        "WebkitTransform": "rotate(17deg)"
    },
    "transform-none-chro-13": {
        "transform": "rotate(-17deg)",
        "MsTransform": "rotate(-17deg)",
        "WebkitTransform": "rotate(-17deg)"
    },
    "chro-14": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 40,
        "left": 385,
        "position": "absolute",
        "marginLeft": 5,
        "width": 17,
        "height": 75,
        "transform": "rotate(-35deg)",
        "MsTransform": "rotate(-35deg)",
        "WebkitTransform": "rotate(-35deg)"
    },
    "transform-none-chro-14": {
        "transform": "rotate(35deg)",
        "MsTransform": "rotate(35deg)",
        "WebkitTransform": "rotate(35deg)"
    },
    "chro-15": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 157,
        "left": 768,
        "position": "absolute",
        "marginLeft": 5,
        "width": 17,
        "height": 34,
        "transform": "rotate(17deg)",
        "MsTransform": "rotate(17deg)",
        "WebkitTransform": "rotate(17deg)"
    },
    "transform-none-chro-15": {
        "transform": "rotate(-17deg)",
        "MsTransform": "rotate(-17deg)",
        "WebkitTransform": "rotate(-17deg)"
    },
    "chro-16": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 114,
        "left": 721,
        "position": "absolute",
        "marginLeft": 5,
        "width": 15,
        "height": 56,
        "transform": "rotate(-25deg)",
        "MsTransform": "rotate(-25deg)",
        "WebkitTransform": "rotate(-25deg)"
    },
    "transform-none-chro-16": {
        "transform": "rotate(25deg)",
        "MsTransform": "rotate(25deg)",
        "WebkitTransform": "rotate(25deg)"
    },
    "chro-17": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 131,
        "left": 675,
        "position": "absolute",
        "marginLeft": 5,
        "width": 20,
        "height": 26,
        "transform": "rotate(-14deg)",
        "MsTransform": "rotate(-14deg)",
        "WebkitTransform": "rotate(-14deg)"
    },
    "transform-none-chro-17": {
        "transform": "rotate(14deg)",
        "MsTransform": "rotate(14deg)",
        "WebkitTransform": "rotate(14deg)"
    },
    "chro-18": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 129,
        "left": 541,
        "position": "absolute",
        "marginLeft": 5,
        "width": 23,
        "height": 65,
        "transform": "rotate(35deg)",
        "MsTransform": "rotate(35deg)",
        "WebkitTransform": "rotate(35deg)"
    },
    "transform-none-chro-18": {
        "transform": "rotate(-35deg)",
        "MsTransform": "rotate(-35deg)",
        "WebkitTransform": "rotate(-35deg)"
    },
    "chro-19": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 185,
        "position": "absolute",
        "marginLeft": 5,
        "width": 15,
        "height": 38,
        "left": 786,
        "transform": "rotate(17deg)",
        "MsTransform": "rotate(17deg)",
        "WebkitTransform": "rotate(17deg)"
    },
    "transform-none-chro-19": {
        "transform": "rotate(-17deg)",
        "MsTransform": "rotate(-17deg)",
        "WebkitTransform": "rotate(-17deg)"
    },
    "chro-20": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 74,
        "left": 452,
        "position": "absolute",
        "marginLeft": 5,
        "width": 20,
        "height": 55,
        "transform": "rotate(-50deg)",
        "MsTransform": "rotate(-50deg)",
        "WebkitTransform": "rotate(-50deg)"
    },
    "transform-none-chro-20": {
        "transform": "rotate(50deg)",
        "MsTransform": "rotate(50deg)",
        "WebkitTransform": "rotate(50deg)"
    },
    "chro-21": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 193,
        "left": 653,
        "position": "absolute",
        "marginLeft": 5,
        "width": 40,
        "height": 21
    },
    "chro-22": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 156,
        "left": 487,
        "position": "absolute",
        "marginLeft": 5,
        "width": 21,
        "height": 64,
        "transform": "rotate(46deg)",
        "MsTransform": "rotate(46deg)",
        "WebkitTransform": "rotate(46deg)"
    },
    "transform-none-chro-22": {
        "transform": "rotate(-46deg)",
        "MsTransform": "rotate(-46deg)",
        "WebkitTransform": "rotate(-46deg)"
    },
    "chro-MT": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 75,
        "left": 776,
        "position": "absolute",
        "marginLeft": 5,
        "width": 78,
        "height": 78
    },
    "chro-X": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 116,
        "left": 620,
        "position": "absolute",
        "marginLeft": 5,
        "width": 16,
        "height": 55
    },
    "chro-Y": {
        "cursor": "pointer",
        "zIndex": 100,
        "top": 129,
        "left": 423,
        "position": "absolute",
        "marginLeft": 5,
        "width": 34,
        "height": 75
    },
    "blue_s ul lihdng_new_type": {
        "height": 78,
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "hdng_new_type": {
        "textAlign": "center",
        "width": 113,
        "lineHeight": 78,
        "verticalAlign": "middle",
        "color": "#fff",
        "fontFamily": "'open_sansbold'",
        "fontSize": 20,
        "marginRight": 20
    },
    "btn-material": {
        "borderRadius": 0
    }
});