class headerStyles():
    headerFlexContainer={
        'marginBottom': '0',
        'marginTop': '0',
        'display': 'flex',
        'alignItems': 'center',
        'width': '100%',
        'justifyContent': 'spaceBetween'
    }
    
    dashboardTitle={
        'color': 'white',
        'marginTop': '0px',
        'marginBottom': '0px',
        'flexBasis': 'content',
        'paddingRight': '10px',
        'paddingLeft': '5px',
        'flex-grow': '1'
    }

    tabStyle={
        'backgroundColor': 'black', 
        'color': 'white', 
        'borderBottomColor': 'black',
        'borderTopLeftRadius': '7px',
        'borderTopRightRadius': '7px',
        'paddingTop': '10px',
        'paddingBottom': '5px',
        'width': 'auto'
    }

    tabSelectedStyle={
        'backgroundColor': '#323232', 
        'color': 'white', 
        'borderBottomColor': 'black', 
        'borderTopColor': 'white',
        'borderTopLeftRadius': '7px',
        'borderTopRightRadius': '7px',
        'paddingTop': '10px',
        'paddingBottom': '5px',
        'width': 'auto'
    }

class engDashboardTab():
    graphGridContainerStyle={
        'display': 'grid',
        'gridTemplate': 'auto repeat(2, 1fr) / repeat(4, 1fr)',
        'width': '100%',
        'border': '1px solid white'
    }

    dataTypeDropdownGridElement={
        'grid-column': '1 / 3',
        'grid-row': '1 / 2'
    }

    timeFrameDropdownGridElement={
        'grid-column': '3 / 5',
        'grid-row': '1 / 2'
    }

    bscGraphContainer={
        'grid-column': '1 / 3',
        'grid-row': '2 / 3'
    }

    rncGraphContainer={
        'grid-column': '3 / 5',
        'grid-row': '2 / 3'
    }

    trxGraphContainer={
        'grid-column': '1 / 5',
        'grid-row': '3 / 4'
    }

class graphStyles():
    plot_bgcolor='#2F2F2F'
    paper_bgcolor='#000000'
    font_color='#FFFFFF'

class topWorstTab():
    datatableGridContainer = {
        'display': 'grid',
        'grid-template': 'auto repeat(5, 1fr) / repeat(2, 1fr)',
        'width': '100%',
        'border': '1px solid white'
    }

    style_header = {
        'backgroundColor':'black',
        'color':'white'
    }

    style_cell = {
        'backgroundColor':'black',
        'color':'white'
    }

class networkCheckTab():
    networkCheckGridContainer = {
        'display': 'grid',
        'grid-template': 'repeat(6, 1fr) / repeat(6, 1fr)',
        'width': '100%',
        'border': '1px solid white'
    }

class NetworkWideGraphColors():
    plot_bgcolor='#2F2F2F'
    paper_bgcolor='#000000'
    font_color='#FFFFFF'
    height=700
    legend_font_size=14
    graphTitleFontSize=20