class gridContainer():
    currentKPIGridContainer = {
        'display':'grid',
        'gridTemplate':' auto repeat(3, 1fr) / repeat(6, 1fr)',
        'gap': '1px',
        'width':'100%'
    }

    gsmGraphGridContainerStyle = {
        'display':'grid',
        'gridTemplate':'repeat(2, 1fr) / repeat(2, 1fr)',
        'width':'100%'
    }

    umtsGraphGridContainerStyle = {
        'display':'grid',
        'gridTemplate':'repeat(2, 1fr) / repeat(3, 1fr)',
        'width':'100%'
    }

    lteGraphGridContainerStyle = {
        'display':'grid',
        'gridTemplate':'repeat(2, 1fr) / repeat(2, 1fr)',
        'width':'100%'
    }

class gridElement():
    gsmCsCssrStyle={
        'grid-column':'1 / 2',
        'grid-row':'1 / 2'
    }

    gsmPsCssrStyle={
        'grid-column':'2 / 3',
        'grid-row':'1 / 2'
    }

    gsmCsDcrStyle={
        'grid-column':'1 / 3',
        'grid-row':'2 / 3'
    }

    lteGeneralKPITableStyle={
        'grid-column':'1 / 2',
        'grid-row':'1 / 2'
    }

    umtsGeneralKPITableStyle={
        'grid-column':'1 / 2',
        'grid-row':'2 / 3'
    }

    gsmGeneralKPITableStyle={
        'grid-column':'1 / 2',
        'grid-row':'3 / 4'
    }

    umtsDcrStyle={
        'grid-column':'1 / 2',
        'grid-row':'1 / 2'
    }

    hsdpaDcrStyle={
        'grid-column':'2 / 3',
        'grid-row':'1 / 2'
    }

    hsupaDcrStyle={
        'grid-column':'3 / 4',
        'grid-row':'1 / 2'
    }

    umtsCssrStyle={
        'grid-column':'1 / 2',
        'grid-row':'2 / 3'
    }

    hsdpaCssrStyle={
        'grid-column':'2 / 3',
        'grid-row':'2 / 3'   
    }

    hsupaCssrStyle={
        'grid-column':'3 / 4',
        'grid-row':'2 / 3'
    }

    lteVolteDcrStyle={
        'grid-column':'1 / 2',
        'grid-row':'1 / 2'
    }

    lteDataDcrStyle={
        'grid-column':'2 / 3',
        'grid-row':'1 / 2'
    }

    lteVolteCssrStyle={
        'grid-column':'1 / 2',
        'grid-row':'2 / 3'
    }

    lteDataCssrStyle={
        'grid-column':'2 / 3',
        'grid-row':'2 / 3'
    }

class NetworkWideGraphColors():
    plot_bgcolor='#2F2F2F'
    paper_bgcolor='#000000'
    font_color='#FFFFFF'
    height=700
    legend_font_size=26
    graphTitleFontSize=52

class datatableHeaderStyle():
    style_header = {
        'backgroundColor':'black',
        'color':'white',
        'fontSize':'24px',
        'whiteSpace': 'normal',
        'height': 'auto'
    }

    style_cell = {
        'backgroundColor':'black',
        'color':'white',
        'fontSize':'24px',
        'whiteSpace': 'normal',
        'height': 'auto'
    }