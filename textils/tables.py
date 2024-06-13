# stdlib dependencies
from typing import List


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
    """

    def array1dToLatexTableRow(array1d, precision=4, end: bool = True):
        if meanstdmode:
            res = " & ".join(
                [f"{val[0]:.{precision}f} pm {val[1]:.{precision}f}" for val in array1d]
            )
            res = res.replace("pm", "$\\pm$")
        else:
            res = " & ".join([f"{val:.{precision}f}" for val in array1d])
        return res + " \\\\" if end else res

    def strListToLatexTableRow(strList, end: bool = True):
        res = " & ".join(strList)
        return res + " \\\\" if end else res

    def intRowsToLatexTableHeader(intRows):
        return " ".join(["|c"] * intRows) + "|"

    def generalstringformatter(strlatex: str) -> str:
        return strlatex.replace("_", "\\_")

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
    formattedTable = generalstringformatter(fullTable)
    with open(outputPath, "w") as f:
        f.write(formattedTable)
