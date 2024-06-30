# stdlib dependencies
from typing import List, Tuple, Dict, Callable
import re


def generateLatexTableFromDataframeLike(
    df_dict,
    outputPath: str,
    maxValueColumns: int = 25,
    caption: str = "Sample Caption",
    label: str = "sample_label",
    precision: int = 4,
    noScientificNotationInterval: Tuple[float, float] = (1e-4, 1e4),
):
    """
    df_dict = df.to_dict(orient='list')
    See generateLatexTable for the rest of the arguments.
    """
    header = list(df_dict.keys())
    numRows = len(next(iter(df_dict.values())))
    numericRowValuesList = [
        [df_dict[col][i] for col in header if isinstance(df_dict[col][i], (int, float))]
        for i in range(numRows)
    ]
    strRowValuesList = [
        [df_dict[col][i] for col in header if isinstance(df_dict[col][i], str)]
        for i in range(numRows)
    ]
    generateLatexTable(
        numericRowValuesList=numericRowValuesList,
        header=header,
        outputPath=outputPath,
        strRowValuesList=strRowValuesList if strRowValuesList[0] != [] else None,
        maxValueColumns=maxValueColumns,
        precision=precision,
        caption=caption,
        label=label,
        noScientificNotationInterval=noScientificNotationInterval,
    )


def generateLatexTable(
    numericRowValuesList: List[List[float]],
    header: List[str],
    outputPath: str,
    strRowValuesList: List[List[str]] = None,
    maxValueColumns: int = 25,
    precision: int = 4,
    caption: str = "Sample Caption",
    label: str = "sample_label",
    meanstdmode: bool = False,
    noScientificNotationInterval: Tuple[float, float] = (1e-4, 1e4),
):
    """
    Args:
        numericRowValuesList:
            if not meanstdmode (default): An element of this list is an array with values for columns.
            else: An element of this list is a list of tuples, each tuple contains the mean and std.
        strRowValuesList: List of lists containing the string values to be displayed in the left hand side columns of the table rows.
        header: column names.
        outputPath:
            Complete filepath for the .tex file.
            Example: ./tables/some_table.tex
        strRowValuesList: List of lists containing the string values to be displayed in the left hand side columns of the table rows.
        maxValueColumns: Maximum number of columns to be displayed in the table.
            if len(header) > maxValueColumns: the columns corresponding to numerical values will be split into multiple rows.
        precision: Number of decimal places to be displayed.
        caption: table caption.
        label: table label.
        meanstdmode: see numericRowValuesList description.
        noScientificNotationInterval: If the absolute value is within this interval, scientific notation will not be used.
    """
    formatNumber = lambda x: (
        f"{x:.{precision}e}"
        if abs(x) < noScientificNotationInterval[0]
        or abs(x) > noScientificNotationInterval[1]
        else f"{x:.{precision}f}"
    )

    def array1dToLatexTableRow(array1d, end: bool = True):
        if meanstdmode:
            res = " & ".join(
                [f"{formatNumber(val[0])} pm {formatNumber(val[1])}" for val in array1d]
            )
            res = res.replace("pm", "$\\pm$")
        else:
            res = " & ".join([formatNumber(val) for val in array1d])
        return res + " \\\\" if end else res

    def strListToLatexTableRow(strList, end: bool = True):
        res = " & ".join(strList)
        return res + " \\\\" if end else res

    def intRowsToLatexTableHeader(intRows):
        return " ".join(["|c"] * intRows) + "|"

    def generalstringformatter(strlatex: str) -> str:
        return strlatex.replace("_", "\\_").replace("%", "\\%")

    def captionLabelStringFormatter(strlatex: str) -> str:
        pattern = re.compile(r'\\(caption|label)\{.*?\}')
        def replaceUnderscore(match):
            content = match.group()
            return re.sub(r'\\_', r'_', content)
        return pattern.sub(replaceUnderscore, strlatex)

    def pipelineStringFormatters(strlatex: str, formatters: List[Callable]) -> str:
        return formatters[0](strlatex) if len(formatters) == 1 else formatters[-1](pipelineStringFormatters(strlatex, formatters[:-1]))

    numFixedColumns = len(strRowValuesList[0]) if strRowValuesList is not None else 0
    effectiveMaxColumns = maxValueColumns - numFixedColumns
    numFullColumns = len(header) - numFixedColumns
    headerSplits = [
        header[i : i + effectiveMaxColumns]
        for i in range(
            numFixedColumns,
            numFullColumns + numFixedColumns,
            effectiveMaxColumns,
        )
    ]
    headerSplits = [header[:numFixedColumns] + split for split in headerSplits]
    numericRowValuesListSplits = []
    for row in numericRowValuesList:
        RowSplits = [
            row[i : i + effectiveMaxColumns]
            for i in range(0, len(row), effectiveMaxColumns)
        ]
        numericRowValuesListSplits.append(RowSplits)
    strRowValuesListRepeated = (
        strRowValuesList * len(headerSplits) if strRowValuesList else None
    )
    tableParts = []
    for idx, header_split in enumerate(headerSplits):
        middle_rows = (
            "\n            ".join(
                [
                    f"{strListToLatexTableRow(strRowValuesListRepeated[i], end=False)} & "
                    + array1dToLatexTableRow(
                        numericRowValuesListSplits[i][idx], precision
                    )
                    for i in range(len(numericRowValuesListSplits))
                ]
            )
            if strRowValuesList
            else "\n            ".join(
                [
                    array1dToLatexTableRow(
                        numericRowValuesListSplits[i][idx], precision
                    )
                    for i in range(len(numericRowValuesListSplits))
                ]
            )
        )
        # bad formatting on purpose
        tablePart = f"""            {strListToLatexTableRow(header_split)}
            \\midrule
            {middle_rows}
            """
        tableParts.append(tablePart)
    middlePart = "\\bottomrule\\midrule".join(tableParts)
    fullTable = f"""
\\begin{{table}}[!ht]
    \\centering
    \\resizebox{{\\textwidth}}{{!}}{{
        \\begin{{tabular}}{{{intRowsToLatexTableHeader(len(headerSplits[0]))}}}
            \\toprule
            {middlePart}
            \\bottomrule
        \\end{{tabular}}
    }}
    \\caption{{{caption}}}
    \\label{{{label}}}
\\end{{table}}
"""
    formattedTable = pipelineStringFormatters(fullTable, [generalstringformatter, captionLabelStringFormatter])
    with open(outputPath, "w") as f:
        f.write(formattedTable)
