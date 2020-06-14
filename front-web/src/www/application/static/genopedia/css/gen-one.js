import React, {StyleSheet, Dimensions, PixelRatio} from "react-native";
const {width, height, scale} = Dimensions.get("window"),
    vw = width / 100,
    vh = height / 100,
    vmin = Math.min(vw, vh),
    vmax = Math.max(vw, vh);

export default StyleSheet.create({
    "chromName": {
        "position": "absolute",
        "left": 45,
        "top": 30,
        "fontSize": 15,
        "fontWeight": "800",
        "color": "#FFF"
    },
    "inner_con_banner": {
        "position": "relative"
    },
    "imgChrom": {
        "maxWidth": "100%"
    },
    "div[class^=\"chrom\"]": {
        "zIndex": 10,
        "cursor": "pointer",
        "position": "absolute"
    },
    "chromLeft": {
        "top": 69,
        "left": 43,
        "width": 72,
        "height": 201
    },
    "chromRight": {
        "top": 69,
        "left": 138,
        "width": 74,
        "height": 201
    },
    "chrom1": {
        "top": 137,
        "left": 322,
        "height": 116,
        "width": 40,
        "transform": "rotate(60deg)"
    },
    "chrom2": {
        "top": 219,
        "left": 361,
        "height": 40,
        "width": 26,
        "transform": "rotate(63deg)"
    },
    "chrom3": {
        "top": 240,
        "left": 451,
        "height": 85,
        "width": 36,
        "transform": "rotate(42deg)"
    },
    "chrom4": {
        "top": 222,
        "left": 533,
        "height": 57,
        "width": 20,
        "transform": "rotate(-27deg)"
    },
    "chrom5": {
        "top": 250,
        "left": 573,
        "height": 25,
        "width": 20
    },
    "chrom6": {
        "top": 188,
        "left": 595,
        "height": 64,
        "width": 17,
        "transform": "rotate(-24deg)"
    },
    "chrom7": {
        "top": 230,
        "left": 676,
        "height": 55,
        "width": 16,
        "transform": "rotate(30deg)"
    },
    "chrom8": {
        "top": 176,
        "left": 723,
        "height": 56,
        "width": 18,
        "transform": "rotate(54deg)"
    },
    "chrom9": {
        "top": 249,
        "left": 717,
        "height": 28,
        "width": 18,
        "transform": "rotate(-46deg)"
    },
    "chrom10": {
        "top": 233,
        "left": 791,
        "height": 36,
        "width": 12,
        "transform": "rotate(-9deg)"
    },
    "chrom11": {
        "top": 169,
        "left": 854,
        "height": 59,
        "width": 14,
        "transform": "rotate(31deg)"
    },
    "chrom12": {
        "top": 181,
        "left": 900,
        "height": 37,
        "width": 5,
        "transform": "rotate(112deg)"
    },
    "chrom13": {
        "top": 177,
        "left": 819,
        "height": 41,
        "width": 9,
        "transform": "rotate(17deg)"
    },
    "chrom14": {
        "top": 44,
        "left": 397,
        "height": 71,
        "width": 11,
        "transform": "rotate(-34deg)"
    },
    "chrom15": {
        "top": 156,
        "left": 773,
        "height": 33,
        "width": 17,
        "transform": "rotate(16deg)"
    },
    "chrom16": {
        "top": 111,
        "left": 726,
        "height": 57,
        "width": 13,
        "transform": "rotate(-25deg)"
    },
    "chrom17": {
        "top": 129,
        "left": 679,
        "height": 27,
        "width": 20,
        "transform": "rotate(0deg)"
    },
    "chrom18": {
        "top": 133,
        "left": 544,
        "height": 65,
        "width": 24,
        "transform": "rotate(25deg)"
    },
    "chrom19": {
        "top": 185,
        "left": 791,
        "height": 40,
        "width": 15,
        "transform": "rotate(25deg)"
    },
    "chrom20": {
        "top": 75,
        "left": 456,
        "height": 54,
        "width": 19,
        "transform": "rotate(-54deg)"
    },
    "chrom21": {
        "top": 185,
        "left": 668,
        "height": 40,
        "width": 20,
        "transform": "rotate(83deg)"
    },
    "chrom22": {
        "top": 155,
        "left": 488,
        "height": 70,
        "width": 21,
        "transform": "rotate(46deg)"
    },
    "chrom23": {
        "top": 129,
        "left": 428,
        "height": 74,
        "width": 32,
        "transform": "rotate(1deg)"
    },
    "chrom24": {
        "top": 120,
        "left": 628,
        "height": 53,
        "width": 10,
        "transform": "rotate(-3deg)"
    },
    "chrom25": {
        "top": 70,
        "left": 788,
        "height": 92,
        "width": 56,
        "transform": "rotate(-34deg)"
    },
    "div[class^=\"connector\"]": {
        "position": "absolute",
        "background": "#FFF",
        "width": 1,
        "cursor": "pointer",
        "zIndex": 10
    },
    "connector-chrom1": {
        "top": 194,
        "left": 275,
        "height": 50,
        "transform": "rotate(60deg)"
    },
    "connector-chrom2": {
        "top": 219,
        "left": 340,
        "height": 58,
        "transform": "rotate(60deg)"
    },
    "connector-chrom3": {
        "top": 255,
        "left": 430,
        "height": 58,
        "transform": "rotate(66deg)"
    },
    "connector-chrom4": {
        "top": 255,
        "left": 524,
        "height": 58,
        "transform": "rotate(46deg)"
    },
    "connector-chrom5": {
        "top": 270,
        "left": 575,
        "height": 45,
        "transform": "rotate(14deg)"
    },
    "connector-chrom6": {
        "top": 246,
        "left": 603,
        "height": 45,
        "transform": "rotate(17deg)"
    },
    "connector-chrom7": {
        "top": 275,
        "left": 680,
        "height": 35,
        "transform": "rotate(-13deg)"
    },
    "connector-chrom8": {
        "top": 210,
        "left": 742,
        "height": 65,
        "transform": "rotate(-13deg)"
    },
    "connector-chrom9": {
        "top": 270,
        "left": 736,
        "height": 50,
        "transform": "rotate(-13deg)"
    },
    "connector-chrom10": {
        "top": 260,
        "left": 806,
        "height": 50,
        "transform": "rotate(-16deg)"
    },
    "connector-chrom11": {
        "top": 211,
        "left": 869,
        "height": 35,
        "transform": "rotate(-50deg)"
    },
    "connector-chrom12": {
        "top": 191,
        "left": 920,
        "height": 86,
        "transform": "rotate(-32deg)"
    },
    "connector-chrom13": {
        "top": 95,
        "left": 864,
        "height": 105,
        "transform": "rotate(45deg)"
    },
    "connector-chrom14": {
        "top": 60,
        "left": 374,
        "height": 47,
        "transform": "rotate(61deg)"
    },
    "connector-chrom15": {
        "top": 85,
        "left": 770,
        "height": 80,
        "transform": "rotate(-13deg)"
    },
    "connector-chrom16": {
        "top": 93,
        "left": 719,
        "height": 30,
        "transform": "rotate(-13deg)"
    },
    "connector-chrom17": {
        "top": 77,
        "left": 678,
        "height": 65,
        "transform": "rotate(-35deg)"
    },
    "connector-chrom18": {
        "top": 78,
        "left": 555,
        "height": 65,
        "transform": "rotate(-8deg)"
    },
    "connector-chrom19": {
        "top": 218,
        "left": 805,
        "height": 37,
        "transform": "rotate(-25deg)"
    },
    "connector-chrom20": {
        "top": 58,
        "left": 443,
        "height": 25,
        "transform": "rotate(-27deg)"
    },
    "connector-chrom21": {
        "top": 210,
        "left": 654,
        "height": 112,
        "transform": "rotate(9deg)"
    },
    "connector-chrom22": {
        "top": 130,
        "left": 518,
        "height": 35,
        "transform": "rotate(5deg)"
    },
    "connector-chrom23": {
        "top": 185,
        "left": 435,
        "height": 48,
        "transform": "rotate(37deg)"
    },
    "connector-chrom24": {
        "top": 96,
        "left": 619,
        "height": 37,
        "transform": "rotate(-46deg)"
    },
    "connector-chrom25": {
        "top": 67,
        "left": 832,
        "height": 31,
        "transform": "rotate(43deg)"
    },
    "connector-organ-0": {
        "top": 0,
        "left": 1250,
        "height": 44,
        "transform": "rotate(90deg)"
    },
    "connector-organ-1": {
        "top": 70,
        "left": 1275,
        "height": 74,
        "transform": "rotate(90deg)"
    },
    "connector-organ-2": {
        "top": 11,
        "left": 1185,
        "height": 50,
        "transform": "rotate(90deg)"
    },
    "connector-organ-3": {
        "top": -7,
        "left": 1262,
        "height": 90,
        "transform": "rotate(90deg)"
    },
    "connector-organ-4": {
        "top": 39,
        "left": 1195,
        "height": 55,
        "transform": "rotate(90deg)"
    },
    "connector-organ-5": {
        "top": 21,
        "left": 1245,
        "height": 54,
        "transform": "rotate(90deg)"
    },
    "connector-organ-13": {
        "top": 45,
        "left": 1275,
        "height": 85,
        "transform": "rotate(90deg)"
    },
    "connector-organ-6": {
        "top": 65,
        "left": 1175,
        "height": 55,
        "transform": "rotate(90deg)"
    },
    "connector-organ-8": {
        "top": 89,
        "left": 1273,
        "height": 100,
        "transform": "rotate(90deg)"
    },
    "connector-organ-9": {
        "top": 101,
        "left": 1164,
        "height": 80,
        "transform": "rotate(90deg)"
    },
    "connector-organ-7": {
        "top": 134,
        "left": 1180,
        "height": 64,
        "transform": "rotate(90deg)"
    },
    "connector-organ-10": {
        "top": 181,
        "left": 1273,
        "height": 45,
        "transform": "rotate(90deg)"
    },
    "connector-organ-11": {
        "top": 240,
        "left": 1280,
        "height": 45,
        "transform": "rotate(90deg)"
    },
    "connector-organ-12": {
        "top": 190,
        "left": 1177,
        "height": 45,
        "transform": "rotate(90deg)"
    },
    "div[class^='connector-text']": {
        "position": "absolute",
        "background": "transparent",
        "fontSize": 12,
        "color": "#FFF",
        "width": 56
    },
    "connector-text-chrom": {
        "top": 225,
        "left": 180,
        "width": "105px !important"
    },
    "connector-text-chrom1": {
        "top": 235,
        "left": 230
    },
    "connector-text-chrom2": {
        "top": 262,
        "left": 307
    },
    "connector-text-chrom3": {
        "top": 295,
        "left": 345
    },
    "connector-text-chrom4": {
        "top": 305,
        "left": 495
    },
    "connector-text-chrom5": {
        "top": 315,
        "left": 560
    },
    "connector-text-chrom6": {
        "top": 290,
        "left": 589
    },
    "connector-text-chrom7": {
        "top": 313,
        "left": 675
    },
    "connector-text-chrom8": {
        "top": 274,
        "left": 745
    },
    "connector-text-chrom9": {
        "top": 320,
        "left": 735
    },
    "connector-text-chrom10": {
        "top": 308,
        "left": 809
    },
    "connector-text-chrom11": {
        "top": 240,
        "left": 855
    },
    "connector-text-chrom12": {
        "top": 269,
        "left": 938
    },
    "connector-text-chrom13": {
        "top": 91,
        "left": 896
    },
    "connector-text-chrom14": {
        "top": 92,
        "left": 292
    },
    "connector-text-chrom15": {
        "top": 68,
        "left": 701
    },
    "connector-text-chrom16": {
        "top": 75,
        "left": 659
    },
    "connector-text-chrom17": {
        "top": 69,
        "left": 597
    },
    "connector-text-chrom18": {
        "top": 63,
        "left": 490
    },
    "connector-text-chrom19": {
        "top": 253,
        "left": 809
    },
    "connector-text-chrom20": {
        "top": 41,
        "left": 431
    },
    "connector-text-chrom21": {
        "top": 321,
        "left": 638
    },
    "connector-text-chrom22": {
        "top": 113,
        "left": 514
    },
    "connector-text-chrom23": {
        "top": 228,
        "left": 413
    },
    "connector-text-chrom24": {
        "top": 87,
        "left": 546
    },
    "connector-text-chrom25": {
        "top": 55,
        "left": 838
    },
    "connector-text-genPairInfo": {
        "top": 80,
        "left": 220
    },
    "connector-text-genPairInfo> p": {
        "width": 100
    },
    "connector-text-organ-0": {
        "top": 11,
        "right": 530
    },
    "connector-text-organ-2": {
        "top": 25,
        "right": 673
    },
    "connector-text-organ-1": {
        "top": 95,
        "right": 490
    },
    "connector-text-organ-3": {
        "top": 29,
        "right": 498
    },
    "connector-text-organ-4": {
        "top": 48,
        "right": 680
    },
    "connector-text-organ-5": {
        "top": 39,
        "right": 534
    },
    "connector-text-organ-13": {
        "top": 76,
        "right": 485
    },
    "connector-text-organ-6": {
        "top": 80,
        "right": 690
    },
    "connector-text-organ-8": {
        "top": 127,
        "right": 477
    },
    "connector-text-organ-9": {
        "top": 120,
        "right": 730
    },
    "connector-text-organ-7": {
        "top": 155,
        "right": 700
    },
    "connector-text-organ-10": {
        "top": 195,
        "right": 506
    },
    "connector-text-organ-11": {
        "top": 252,
        "right": 500
    },
    "connector-text-organ-12": {
        "top": 200,
        "right": 685
    }
});