# -*- coding: utf-8 -*-

import base64
import cgitb
import ctypes
import datetime
import glob
import hashlib
import json
import os
import time
import textwrap
import pypandoc
import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import *
from qframelesswindow.webengine import FramelessWebEngineView
from selenium import webdriver
from urllib.parse import urlencode
from deepdiff import DeepDiff
from win10toast import ToastNotifier

VERSION = "v4.0-PreRelease"
FILEDIR = "C:/ZhiXueHacker"

# 创建图标
zhixueIcon = b'AAABAAEAAAAAAAEAIACVHQAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAEAAAABAAgGAAAAXHKoZgAAAAlwSFlzAAAOxAAADsQBlSsOGwAAC8dpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDkuMC1jMDAxIDc5LmMwMjA0YjIsIDIwMjMvMDIvMDktMDY6MjY6MTQgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIiB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjQuMyAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDI0LTA1LTAxVDE2OjA3OjQ0KzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyNC0wNS0wNVQyMDowODoxNyswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyNC0wNS0wNVQyMDowODoxNyswODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6NzI1MTNmNzgtMDhkMi00ODQxLTgzZmItNGFkOWQ1OGNiYzViIiB4bXBNTTpEb2N1bWVudElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6MjJiMTc3M2MtMDE5MS02MjQ3LThmNmUtODNiMWFkNWJjZmM5IiB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ODM5YmEyNjgtOTExMC0wOTRkLTkxYTYtMmVmMWY2MmM1NTI1Ij4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo4MzliYTI2OC05MTEwLTA5NGQtOTFhNi0yZWYxZjYyYzU1MjUiIHN0RXZ0OndoZW49IjIwMjQtMDUtMDFUMTY6MDc6NDQrMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyNC4zIChXaW5kb3dzKSIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6ZjYwMmVjZTAtY2JjZi1iMDQ3LWEwNWItNTQwOTZhMTU0Yjg3IiBzdEV2dDp3aGVuPSIyMDI0LTA1LTAxVDE2OjEwOjM4KzA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgMjQuMyAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249InNhdmVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjA1ZDg4MTIwLTMwMTUtZDI0ZS1iYWVjLTMwMzk1ZDE0YWM5YyIgc3RFdnQ6d2hlbj0iMjAyNC0wNS0wNVQyMDowODowOSswODowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDI0LjMgKFdpbmRvd3MpIiBzdEV2dDpjaGFuZ2VkPSIvIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjb252ZXJ0ZWQiIHN0RXZ0OnBhcmFtZXRlcnM9ImZyb20gaW1hZ2UvcG5nIHRvIGFwcGxpY2F0aW9uL3ZuZC5hZG9iZS5waG90b3Nob3AiLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249ImRlcml2ZWQiIHN0RXZ0OnBhcmFtZXRlcnM9ImNvbnZlcnRlZCBmcm9tIGltYWdlL3BuZyB0byBhcHBsaWNhdGlvbi92bmQuYWRvYmUucGhvdG9zaG9wIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo1OGI1ODUwZC05Nzk0LWFmNGEtODdjMC1iZmM0ZDVkZjc1MDEiIHN0RXZ0OndoZW49IjIwMjQtMDUtMDVUMjA6MDg6MDkrMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyNC4zIChXaW5kb3dzKSIgc3RFdnQ6Y2hhbmdlZD0iLyIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6NGY2ODA2N2EtMjFlMC00NTQ2LWE4NjMtOGM1OWFiMzUyZTBiIiBzdEV2dDp3aGVuPSIyMDI0LTA1LTA1VDIwOjA4OjE3KzA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgMjQuMyAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249ImNvbnZlcnRlZCIgc3RFdnQ6cGFyYW1ldGVycz0iZnJvbSBhcHBsaWNhdGlvbi92bmQuYWRvYmUucGhvdG9zaG9wIHRvIGltYWdlL3BuZyIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iZGVyaXZlZCIgc3RFdnQ6cGFyYW1ldGVycz0iY29udmVydGVkIGZyb20gYXBwbGljYXRpb24vdm5kLmFkb2JlLnBob3Rvc2hvcCB0byBpbWFnZS9wbmciLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249InNhdmVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjcyNTEzZjc4LTA4ZDItNDg0MS04M2ZiLTRhZDlkNThjYmM1YiIgc3RFdnQ6d2hlbj0iMjAyNC0wNS0wNVQyMDowODoxNyswODowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDI0LjMgKFdpbmRvd3MpIiBzdEV2dDpjaGFuZ2VkPSIvIi8+IDwvcmRmOlNlcT4gPC94bXBNTTpIaXN0b3J5PiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDo0ZjY4MDY3YS0yMWUwLTQ1NDYtYTg2My04YzU5YWIzNTJlMGIiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6NThiNTg1MGQtOTc5NC1hZjRhLTg3YzAtYmZjNGQ1ZGY3NTAxIiBzdFJlZjpvcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ODM5YmEyNjgtOTExMC0wOTRkLTkxYTYtMmVmMWY2MmM1NTI1Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+Bql1vAAAEXRJREFUeJzt3XmwT/Ufx/FzLYnGnq+tZFowltLCqCwhofqZLKmJyghNKaSGlGba+FV0RSk0yjLTiEZdxpqIJnK71oyylmS7ZSmVyPL74zf37X3O3Ht9Odv3e9/Px1+vc7/f7zkft9t7Pp/v+ZzPJ8MpQCKR+I/nR0+qfJPKFQs6B4DQHVE5R+VM/abc3NwF+X24RBgtApAeKACAYRn6IJFIvKwOX4i4LQDC81JeyM3NfTEv0wMADKMAAIZlJBKJO9XxvNhaAiAqd+cFegCAYRQAwLASjuMMjrsRACL1dF6gBwAYRgEADKMAAIaVcBynSdyNABApeZiPHgBgGAUAMKyE4zjl4m4EgEiVzQv0AADDKACAYRQAwDAKAGAYBQAwjAIAGEYBAAyjAACGUQAAwygAgGEUAMAwCgBgGAUAMIwCABhGAQAMowAAhlEAAMMoAIBhFADAMAoAYBgFADCMAgAYRgEADKMAAIZRAADDKACAYRQAwDAKAGAYBQAwjAIAGEYBAAyjAACGUQAAwygAgGEUAJy3jIwMye3atZP80EMPSW7YsKHrM2XKlJGck5Mj+YUXXpC8Y8eOQNuJc6MAAIZRAADDMhKJxJm4G4HUV716dclTpkyR3LhxY1/n3bVrl+TmzZtLPnHihK/zIjn0AADDKACAYRSANNGiRQvJ+hv27du3S162bJnkkydP+rqe7vI7juMsXLhQcrVq1XydW7viiiskN2rUSPKaNWsCuwYKRgEADKMAAIZRAFLUfffd5zoeN27cOT/z888/S37iiSdcr61evfqcn9cTfCZMmOB6Lchuf0GOHj0a+jXgRgEADKMAAIZRAFKUnhSTrFq1akmeNWuW67W7775b8saNG/P9fPv27SU3a9bsvK9/IRYvXix569atkVwTZ1EAAMMoAIBhFIAUpSfeOI7jdOvWTXKxYsXO+flSpUq5jkeNGiVZd/W13r17J9W233//XfJPP/0k+dixY/lmx3GcI0eOSM7OzpY8bdq0pK6JcFAAAMMoAIBhFADAMNYDSBP16tWT3KRJE8n6oZ0qVapIvvnmm12fv+aaayTffvvtknfu3ClZ34ZbunSp6/OZmZmS161bd15tR+qiBwAYRgEADDMzBChZsqTkBg0aSK5bt67kChUqSK5YsaLr8/q1U6dOST548GC++bfffnN9fs+ePZI3bdok2e9z+8nq2bOn5Isvvljyd999J7lt27aSR44cGUm79ANIderUkVy7dm3X+ypXrixZD3X0z0uXLi1Z33b0Hh8+fFjyjz/+KHnDhg2S//7776Tan+7oAQCGUQAAw9J+CFC/fn3JXbt2lex9mEUvN+WdJRe1v/76S7J+Tv/rr7+WvHz5ctdndFfdr5o1a+b7871790o+c8bfn4Ve6stxHKd169aSb7311nyz7s7HQQ/ttmzZ4nrt22+/lZyVlSV55cqVkv3+zuJADwAwjAIAGJayQ4CyZcu6jvW32N27d5eshwBF2fr16yVPnDhR8ty5cyX/+++/kbbJcRynZcuWkvv16ydZTzZyHPe3/UWJHjbpNRj05ine96USegCAYRQAwLDYhwD6G3n9PPrAgQNd7/NOzMH/7d+/X7IeGrz//vuu9/kdHnTu3FnyoEGDJOtnFHDW8ePHXccffvih5LFjx0o+dOhQZG3KDz0AwDAKAGBY7EOARYsWSfa71TTO2rx5s+v4qaeekqzvKGh6gpBeQsxx3M8JwB+9pNr1118vWU8Qiwo9AMAwCgBgWOwFQM95ZwgQHO8Eqfnz50ueNGmSZP2Y8rBhwyRfcsklIbbOtrVr10qOo9uvxV4AAMSHAgAYRgEADIv9NqBe+umbb76RXFQfHgH69OkjWT/MFQd6AIBhFADAsNgLgN5ccurUqZJ79eoVfWOAkOTk5EieN29ejC1xi70AAIgPBQAwLPa7AJqefbZixQrXa5dddlnUzSnQr7/+KlnPpDtw4IBk78YSej2DGjVqSNZ79lm887F7927Ju3btkqw3WXEcxylevLjkqlWrStZ7I6bS34h3PYA2bdpI3r59e9TNKRA9AMAwCgBgWEoVAN1t/v77712vRdG90/vE6RVeHcdxFixYINn7rL0fes/B5s2bS+7Ro4frfbfddpvkYsWKBXb9sHjXHJg+fbrkL774QvK+ffsCu6b+G+nYsaPrtS5duki+4YYbArtmQbyrAAf57wxSShUAANGiAACGpdRdgKFDh0oePHhwaNfRW3ePHj1asu6mRrVtd7L06rt66269t14ctm3bJvn555+X7N3bMJV06NBB8vDhwyXrOzJB00vf6Ulup0+fDu2ayaAHABhGAQAMi30IoDecmDBhQmjX0ds46w1IDh8+HNo1o6AfLX3ppZcklygRXm3X+97pLnQcexP6VbJkScmvv/66ZO9dmCCNHz9e8ssvvxzadZJBDwAwjAIAGEYBAAyL5TuASy+9VHJ2drbkIJei/uijj1zHQ4YMkZyOY9VktGrVSrK+pek47k1YL4Qe63s3Hi2KHn30UddxWGP1Tp06SV69enUo1ygMPQDAMAoAYFgsQwB9uyXIpb+WLFki+cEHH3S9FveMq6h5H4aZPHmyZP1sfUHeeOMN1/Gbb74ZTMPS1HPPPSd54MCBgZ1X7xLk/W8WBXoAgGEUAMCwyIYA+kGLL7/8UrLfGWs7duyQ3L59e8lHjx71dd6iRj+oM2DAgHzfs2zZMsn3339/6G1KJ3q5Nn2HpV27doFdo2/fvpLnzJkT2HkLQw8AMIwCABgW2RAgMzNTcpAPWjzwwAOS9VJTcNMPveiufs2aNSXrtQW8S1rhLL302KpVqyRfdNFFvs67ceNGyUEOLQpDDwAwjAIAGBZaAfCuXKuXYfJLP9tPtz85+vmHMWPGSL722msl0+1Pzi+//CJZT7B67LHHfJ1X/7fwroKtrxkkegCAYRQAwLDQ7gI0a9bMdZyVlRXYufU8/8WLFwd2Xiv0swDly5eXfOjQoTiak9b0Po96Xr/ffR7149eOE94j2PQAAMMoAIBhFADAsNAKgH4wJwh649BU3nUmHZw6dUoy435/9K3TDRs2SG7cuLGv83pvm/MdAIDAUQAAw0IrAFdffXWg51uxYoXk48ePB3ruMHgf5mjSpInk3bt3S/7kk08kHzt2LPyGpQB9i0yvituwYUPJetNRx3Gc2bNnS061jVvz6FvSfocAV111ld/mJIUeAGAYBQAwLLQCULVq1UDPp5f+SlV6Jd2HH344qc/oDSj0N79//vlncA1LMVOnTpWc7N0iPfuzS5cuklNpk5cg/0arVKkS2LkKQw8AMIwCABgWWgGoVq1aoOc7cOBAoOcLSoMGDSQn2+3X9GrJffr0kfzWW2/5a1iKadu2reQLmSTWtGlTyV27dpU8Y8YMfw0LUJB/o35Xy076OpFcBUBKogAAhoVWACpVqhTo+Q4fPhzo+YKiu/B+1a1bN7BzpZo6deqk5LmClKp/o4WhBwAYRgEADAutABw8eNB17PeuQNBDiqBs3rxZ8pkzZ1dXu5AloTZt2hRIm1JRkP+2VP09perfaGHoAQCGUQAAwygAgGGhFYD9+/e7jv1+BxD0zMKgbN26VfLbb78tecCAAUl9fv369ZL1LjNFzVdffSV55syZkrt3757U5/UOUJ999llwDQtQkH+jUa15QA8AMIwCABgWWgEI+uGdoJcYC8OIESMkf/75567XCloSbMGCBZJT6dn2MD355JOS9ZJojRo1kqyHVo7j/n3q262pJMhZobm5uYGdqzD0AADDKACAYaEVgC1btriO/W4U0rJlS8llypSRrDcMSSXZ2dmFHuP/9CYv6b7hS5Cb4XiHQGGhBwAYRgEADAutACxcuNB1nOzEmIKUKlVKcuvWrSXPmzfP13ktKlmypOTKlStL9k7ewrldfvnlkvXycH55//8JCz0AwDAKAGBYaAVg7dq1rmM9sSGRSPg69+OPPy6ZIcD5u/feeyXryTfDhg2LozlprX///qGcd9GiRaGc14seAGAYBQAwLCORSEQysfpC9s1LRu/evSUzHChY6dKlJesJN/oR1hYtWkjetWtXNA1LQ1deeaVk/Ziz38081q1bJ1nvExkmegCAYRQAwDAKAGBYZN8B1KpVS/LKlSsl61lpF0I/W9+uXTvJ6bhLS5heffVVyX379s33PatWrZLcpUsX12unT58Op2FpQo/vP/74Y8nNmzcP7Bo9e/aU7F1PIiz0AADDKACAYZENAbRXXnlFcr9+/QI7rx5aeFebtbLcVp5u3bq5jt955x3Jyexa9N5777mOX3zxxUDala5Gjhwp+ZFHHgnsvHrYdc899wR23mTRAwAMowAAhsUyBKhYsaJkvVRWuXLlArvGnDlzXMd6Jdp//vknsOukkrvuukvypEmTXK/5naU2atQoyaNHj/Z1rlSlh0bPPPOM6zXvsR96VeM777xTsvcBuijQAwAMowAAhsUyBND05J1p06ZJLlasWKDX0Xvw9erVS/K+ffsCvU4U9O9m0KBBkocMGSI5mW/6L9Ts2bMlDx48WPKxY8dCu2ZY9ENS48aNk9ypU6fQrvnaa69JHjNmTGjXSQY9AMAwCgBgWOxDAE1/Uz98+PDQrnP06FHJekvviRMnSk61OwU33XSTZD0p5brrroujOWLPnj2S9WShuXPnut4X935+etikJ0k9++yzkmvWrBna9bOysiQHOfnNL3oAgGEUAMCwlBoCaJmZma7jHj16hH5NvaX5p59+6npNb9SgJy+dOnXK1zV1t7NVq1aS9aOhjuM4N954o6/rRG3nzp2u4+nTp0tesmSJ5G3btkn2O0yoX7++5I4dO7pe69y5s+Qgt/EuiHcvSL0ScyoNL+kBAIZRAADDUnYI4KX3FtQbWAQ9YSgZesKLnkik99bzblteqVIlydWrV883W3TkyBHJeiXiQ4cOud5XvHhxyXol46pVq0ouX758GE1M2syZMyU//fTTrtdOnDgRdXOSQg8AMIwCABhGAQAMS5vvALQ77rhD8rvvviu5bNmycTQHxpw8eVLyiBEjJOu/xXRBDwAwjAIAGJaWQwCtcuXKkvWz6d4NSP1uQJJK5s+fL3nWrFmSx44dKznI5dUcx70xiF4eS8++07/zovT7dhz3xrP6Yazt27fH0ZzA0AMADKMAAIal/RCgILVr13Yd65mE+kERPUMvbnqGoe5yOo7jfPDBB5LXrFmT7+dvueUWyTNmzHC9VqpUKV9tGzp0qOQpU6bk+x79O+/Tp4/rta5du0pOpd+5nrG5bNkyyd5v9HNyciJrU5ToAQCGUQAAw4rsEKAw+sGSJk2aSO7QoYPkevXquT6jHzrRD6PoTU70c97e7cn37t0rWXfhdV66dKlkvWzZhWjTpo3rePz48ZIL6oLrB1a8ewFOnjzZV3v0XYGWLVtKbtq0qWS95oF3CFehQgXJesLXH3/8IVmv56Cz47jXJ9Bbby9fvlzy8ePHC/9HFEH0AADDKACAYSaHAEHS6xHoyTKppkqVKpL1cms1atSQ3L9/f8k//PBDNA27AOnyO08H9AAAwygAgGEMAYzTewjGvXkHokcPADCMAgAYRgEADKMAGMe43zYKAGAYBQAwjAIAGEYBAAyjAACGUQAAwygAgGEUAMAwCgBgGAUAMIwCABhGAQAMowAAhlEAAMMoAIBhFADAMAoAYBgFADCMAgAYRgEADKMAAIZRAADDKACAYRQAwDAKAGAYBQAwjAIAGEYBAAyjAACGUQAAw0o4jvOHOi4XV0MARObPvEAPADCMAgAYVsJxnDXquHVcDQEQmW/zAj0AwDAKAGAYBQAwrITjOGPUMd8BAEXfW3mBHgBgGAUAMCxDHyQSiVfU4fCI2wIgPP/NC7m5uc/lZXoAgGEUAMCwjIJeSCQS//H86CmVm6p8SaAtAnA+/lI5W+Wx+k25ublZ+X2YHgBgGAUAMOx/6VJ39mGK2IoAAAAASUVORK5CYII='
if not os.path.exists(FILEDIR):
    os.mkdir(FILEDIR)
with open(FILEDIR + "/ZhiXueIcon.ico", "wb") as f:
    f.write(base64.b64decode(zhixueIcon))


# Win11云母效果
def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ZhiXueHacker")
sys.excepthook = cgitb.Hook(1, None, 5, sys.stderr, 'text')


class Config(QConfig):
    mica = ConfigItem("Personalization", "Mica", True, BoolValidator(), restart=True)
    theme = OptionsConfigItem("Personalization", "Theme", "Auto", OptionsValidator(["Light", "Dark", "Auto"]),
                              restart=True)
    exportFolder = ConfigItem("Main", "ExportFolder", "export", FolderValidator())
    savePassword = ConfigItem("Main", "SavePassword", False, BoolValidator())
    autoSync = ConfigItem("Main", "AutoSync", True, BoolValidator())
    newScoreMsg = ConfigItem("Main", "NewScoreMsg", True, BoolValidator())
    loginMethod = OptionsConfigItem(
        "Advanced", "LoginMethod", "WebEngineView", OptionsValidator(["WebEngineView", "Selenium", "手动填入 Cookie"]))
    renderMethod = OptionsConfigItem(
        "Advanced", "RenderMethod", "OpenGLES", OptionsValidator(["DesktopOpenGL", "OpenGLES", "SoftwareOpenGL"]), restart=True)


cfg = Config()
qconfig.load(FILEDIR + "/config.json", cfg)

DARKQSS = '''Widget > QLabel {
    font: 24px 'Segoe UI', 'Microsoft YaHei';
}

Widget {
    border-left: 1px solid rgb(29, 29, 29);
    background-color: rgb(39, 39, 39);
}


* {
    background-color: rgb(39, 39, 39);
}

QLabel {
    background-color: transparent;
}

MSFluentTitleBar, CustomTitleBar {
    background-color: transparent;
}

MSFluentTitleBar > QLabel,
Widget > QLabel,
CustomTitleBar > QLabel {
    color: white;
}


MSFluentTitleBar>QLabel#titleLabel, CustomTitleBar>QLabel#titleLabel {
    background: transparent;
    font: 13px 'Segoe UI';
    padding: 0 4px
}



MinimizeButton {
    qproperty-normalColor: white;
    qproperty-normalBackgroundColor: transparent;
    qproperty-hoverColor: white;
    qproperty-hoverBackgroundColor: rgba(255, 255, 255, 26);
    qproperty-pressedColor: white;
    qproperty-pressedBackgroundColor: rgba(255, 255, 255, 51)
}


MaximizeButton {
    qproperty-normalColor: white;
    qproperty-normalBackgroundColor: transparent;
    qproperty-hoverColor: white;
    qproperty-hoverBackgroundColor: rgba(255, 255, 255, 26);
    qproperty-pressedColor: white;
    qproperty-pressedBackgroundColor: rgba(255, 255, 255, 51)
}

CloseButton {
    qproperty-normalColor: white;
    qproperty-normalBackgroundColor: transparent;
}
'''

LIGHTQSS = '''
Widget > QLabel {
    font: 24px 'Segoe UI', 'Microsoft YaHei';
}

Widget {
    border-left: 1px solid rgb(229, 229, 229);
    background-color: rgb(249, 249, 249);
}

StackWidget {
    background-color: rgb(243, 243, 243);
}

MSFluentTitleBar > QLabel#titleLabel, CustomTitleBar > QLabel#titleLabel {
    background: transparent;
    font: 13px 'Segoe UI';
    padding: 0 4px
}
'''

ROLES = ["一评", "二评", "三评", "四评", "五评", "六评", "七评", "八评", "九评"]


class MicaWindow(Window):
    def __init__(self):
        super().__init__()
        self.setTitleBar(MSFluentTitleBar(self))
        self.titleBar.minBtn.hide()
        self.titleBar.maxBtn.hide()
        if isWin11():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())


windowOffset = 0

if cfg.get(cfg.mica):
    WindowType = MicaWindow
else:
    WindowType = FramelessWindow
    windowOffset = 40


class LoginSelenium(QThread):
    callback = pyqtSignal(bool, str)

    def run(self):
        try:
            options = webdriver.EdgeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            browser = webdriver.Edge(options=options)
            browser.maximize_window()
            browser.get("https://www.zhixue.com/login.html")
            print("请在网页端进行登录")
            while browser.current_url != "https://www.zhixue.com/htm-vessel/#/":
                pass
            cookies = browser.get_cookies()
            browser.close()
            with open(FILEDIR + "/cookies.json", "w", encoding="utf-8") as f:
                json.dump(cookies, f)
            print(cookies)
            self.callback.emit(True, "")
        except Exception as e:
            print(e)
            self.callback.emit(False, str(e) + "\n...")


class GetToken(QThread):
    callback = pyqtSignal(bool, str, str, str, str)

    def run(self):
        try:
            with open(FILEDIR + "/cookies.json", "r", encoding="utf-8") as f:
                cookies = json.load(f)
            print(cookies)
            JSESSIONID = None
            tlsysSessionId = None
            for i in cookies:
                if i['name'] == "JSESSIONID" and i['path'] == "/":
                    JSESSIONID = i['value']
                    print("已获取JSESSIONID：", i['value'])
                if i['name'] == "tlsysSessionId":
                    tlsysSessionId = i['value']
                    print("已获取tlsysSessionId：", i['value'])
            token = requests.get(url="https://www.zhixue.com/container/app/token/getToken",
                                 cookies={"JSESSIONID": JSESSIONID, "tlsysSessionId": tlsysSessionId}).json()
            print(token)
            if token['success']:
                print("已获取Token：", token['result'])
                username = requests.get(
                    url="https://www.zhixue.com/container/container/student/account/",
                    cookies={"JSESSIONID": JSESSIONID, "tlsysSessionId": tlsysSessionId}).json()
                print(username)
                self.callback.emit(True, JSESSIONID, tlsysSessionId, token['result'], username['student']['name'])
            else:
                print("Token获取失败，", token['errorInfo'], "，请重新登录")
                os.remove(FILEDIR + "/cookies.json")
                self.callback.emit(False, token['errorInfo'], "", "", "")
        except Exception as e:
            self.callback.emit(False, str(e), "", "", "")


class FetchExam(QThread):
    callback = pyqtSignal(bool, str, list, bool)

    def setPat(self, token, page):
        self.token = token
        self.page = page

    def run(self):
        try:
            s = requests.get(
                url="https://www.zhixue.com/zhixuebao/report/exam/getUserExamList?pageIndex=" + str(
                    self.page) + "&pageSize=10",
                headers={"XToken": self.token}).json()['result']
            print(s)
            next = s['hasNextPage']
            self.callback.emit(True, "", s['examList'], next)
        except Exception as e:
            self.callback.emit(False, str(e), [], False)


class FetchPaper(QThread):
    callback = pyqtSignal(bool, str, list, dict)

    def setPat(self, token, examId):
        self.token = token
        self.examId = examId

    def run(self):
        try:
            subjectRank = {}
            paperList = requests.get(
                url="https://www.zhixue.com/zhixuebao/report/exam/getReportMain?examId=" + self.examId,
                headers={"XToken": self.token}).json()['result']['paperList']
            print(paperList)
            for i in paperList:
                subjectRank[i['subjectCode']] = {'rank': None, 'classTotal': None, 'gradeTotal': None,
                                                 'rankMulti': None}
            try:
                s = \
                    requests.get(
                        "https://www.zhixue.com/zhixuebao/report/exam/getSubjectDiagnosis?examId=" + self.examId,
                        headers={"XToken": self.token}).json()['result']['list']
                print(s)
                for i in s:
                    subjectRank[i['subjectCode']]['rankMulti'] = i['myRank']
                print(subjectRank)
            except:
                print("排名获取失败")
            self.callback.emit(True, "", paperList, subjectRank)
        except Exception as e:
            self.callback.emit(False, str(e), [], {})


class PaperDiff(QThread):
    callback = pyqtSignal(bool, str, list, str, int)

    def setPat(self, token, examId, examName, rowId):
        self.token = token
        self.examId = examId
        self.examName = examName
        self.rowId = rowId

    def run(self):
        while True:
            if not (self.token and self.examId and self.examName):
                time.sleep(0.5)
                continue
            try:
                paperList = requests.get(
                    url="https://www.zhixue.com/zhixuebao/report/exam/getReportMain?examId=" + self.examId,
                    headers={"XToken": self.token}).json()['result']['paperList']
                examFile = FILEDIR + "/record-" + self.examId + ".json"
                print(paperList)
                check = glob.glob(FILEDIR + "/record-*.json")
                newSubject = []
                if check:
                    if os.path.exists(examFile):
                        f = eval(open(examFile, "r", encoding="utf-8").read())
                        diff = DeepDiff(f, paperList, ignore_order=True)
                        print(diff)
                        if 'iterable_item_added' in diff:
                            for i in diff['iterable_item_added'].values():
                                print(i['subjectName'])
                                newSubject.append(i['subjectName'])
                    else:
                        print("NewExam")
                        for i in paperList:
                            print(i['subjectName'])
                            newSubject.append(i['subjectName'])
                with open(examFile, "w", encoding="utf-8") as f:
                    f.write(str(paperList))
                self.callback.emit(True, "", newSubject, self.examName, self.rowId)
            except Exception as e:
                self.callback.emit(False, str(e), [], "", -1)
            time.sleep(60)


class FetchRank(QThread):
    callback = pyqtSignal(bool, str, dict)
    sheetCallback = pyqtSignal(bool, str, list)
    scoreDetailCallback = pyqtSignal(bool, str, list)
    problemCallback = pyqtSignal(bool, str, list)

    def setPat(self, token, examId, paperId, subjectRank, subjectCode, JSESSIONID, tlsysSessionId):
        self.token = token
        self.examId = examId
        self.paperId = paperId
        self.subjectRank = subjectRank
        self.subjectCode = subjectCode
        self.JSESSIONID = JSESSIONID
        self.tlsysSessionId = tlsysSessionId

    def run(self):
        try:
            s = requests.get(
                "https://www.zhixue.com/zhixuebao/report/paper/getLevelTrend?examId=" + self.examId + "&pageIndex=1&pageSize=5&paperId=" +
                self.paperId, headers={"XToken": self.token}).json()['result']['list']
            print(s)
            for j in s[0]['dataList']:
                if j['id'] == self.paperId:
                    try:
                        deltaMin = 1000
                        for i in range(1, j['totalNum'] + 1):
                            rank = 100 / (j['totalNum'] - 1) * (i - 1)
                            delta = abs(self.subjectRank[self.subjectCode]['rankMulti'] - rank)
                            print("pos:", i, "rank:", rank, "delta:", delta)
                            if delta < deltaMin:
                                self.subjectRank[self.subjectCode]['rank'] = i
                                deltaMin = delta
                    except:
                        pass
                    self.subjectRank[self.subjectCode]['classTotal'] = j['totalNum']
            for j in s[1]['dataList']:
                if j['id'] == self.paperId:
                    self.subjectRank[self.subjectCode]['gradeTotal'] = j['totalNum']
            self.callback.emit(True, "", self.subjectRank[self.subjectCode])
        except Exception as e:
            self.callback.emit(False, str(e), {})
            return
        try:
            s = requests.get(
                "https://www.zhixue.com/zhixuebao/report/checksheet/?examId=" + self.examId + "&paperId=" + self.paperId,
                headers={"XToken": self.token}).json()['result']
            print(s)
            orgPaper = eval(s['sheetImages'])
            self.sheetCallback.emit(True, "", orgPaper)
        except Exception as e:
            self.sheetCallback.emit(False, str(e), [])
        try:
            s = requests.get(
                "https://www.zhixue.com/zhixuebao/report/checksheet/?examId=" + self.examId + "&paperId=" + self.paperId,
                headers={"XToken": self.token}).json()['result']
            print(s)
            scoreDetail = \
                eval(s['sheetDatas'].replace("true", "True").replace("false", "False").replace("null", "None"))[
                    'userAnswerRecordDTO']['answerRecordDetails']
            self.scoreDetailCallback.emit(True, "", scoreDetail)
        except Exception as e:
            self.scoreDetailCallback.emit(False, str(e), [])
        try:
            s = requests.get(
                "https://www.zhixue.com/zhixuebao/zhixuebao/transcript/analysis/main/?paperId=" + self.paperId + "&examId=" + self.examId + "&token=" + self.token + "&subjectCode=" + self.subjectCode,
                cookies={"JSESSIONID": self.JSESSIONID, "tlsysSessionId": self.tlsysSessionId}).text
            soup = BeautifulSoup(s, "html.parser")
            js_tag = soup.find_all(name="script")
            detail = []
            for i in js_tag:
                for j in i.text.split("\n"):
                    if 'hisQueParseDetail' in j:
                        detail = eval(
                            j.replace("    var hisQueParseDetail = ", "").rstrip(";").replace("true", "True").replace(
                                "false",
                                "False"))
            if not detail:
                self.problemCallback.emit(False, "无法找到变量 hisQueParseDetail。\n这可能是由于登录过期。请重新登录。",
                                          [])
            else:
                self.problemCallback.emit(True, "", detail)
        except Exception as e:
            self.problemCallback.emit(False, str(e), [])


class DownloadSheet(QThread):
    callback = pyqtSignal(bool, str)

    def setPat(self, exportPath, selectList):
        self.exportPath = exportPath
        self.selectList = selectList

    def run(self):
        try:
            if not os.path.exists(self.exportPath):
                os.mkdir(self.exportPath)
            for i in self.selectList:
                print("开始下载", i)
                respond = requests.head(i)
                if respond.headers.get('Content-Type') == 'image/jpeg':
                    self.callback.emit(False,
                                       "Content-Type 为 " + respond.headers.get(
                                           'Content-Type') + "，预期为 image/jpeg。这可能是由于 URL 已过期。请重新获取。")
                    break
                s = requests.get(i)
                md5 = hashlib.md5(i.encode())
                filename = md5.hexdigest()
                with open(self.exportPath + "/" + filename + ".png", "wb") as f:
                    f.write(s.content)
                print("下载成功")
            self.callback.emit(True, "")
        except Exception as e:
            self.callback.emit(False, str(e))


class GeneratePaper(QThread):
    callback = pyqtSignal(bool, str)

    def setPat(self, exportPath, problemList, title, option):
        self.exportPath = exportPath
        self.problemList = problemList
        self.title = title
        self.option = option

    def run(self):
        try:
            if not os.path.exists(self.exportPath):
                os.mkdir(self.exportPath)
            htmlExport = self.title
            errs = 0
            for i in self.problemList:
                htmlExport += "<h2><b>" + i['topicType'] + "</b></h2>"
                for j in i['topicAnalysisDTOs']:
                    htmlTemp = "<b>" + j['disTitleNumber'] + ". </b>"
                    if self.option[0][0] and self.option[1][0]:
                        htmlTemp += "(" + str(j['score']) + "/" + str(j['standardScore']) + "分) "
                    elif self.option[0][0] and not self.option[1][0]:
                        htmlTemp += "(本题得分 " + str(j['score']) + "分) "
                    elif (not self.option[0][0]) and self.option[1][0]:
                        htmlTemp += "(" + str(j['standardScore']) + "分) "
                    try:
                        htmlTemp += j['content']['accessories'][0]['desc']
                        for opt in j['content']['accessories'][0]['options']:
                            htmlTemp += opt['id'] + "." + opt['desc'] + "<br/>"
                    except:
                        errs += 1
                    for i in range(2, 6):
                        if self.option[i][0] and not self.option[i][1]:
                            print(1)
                            htmlTemp += "<br/><br/>"
                            break
                    try:
                        if self.option[2][0] and not self.option[2][1]:
                            if not j['userAnswer']:
                                j['userAnswer'] = "未作答"
                            htmlTemp += "【你的选择】 " + j['userAnswer'] + "<br/>"
                    except:
                        pass
                    if self.option[3][0] and not self.option[3][1]:
                        htmlTemp += "【答案】" + j['answerHtml'] + "<br/>"
                    if self.option[4][0] and not self.option[4][1]:
                        try:
                            htmlTemp += "【班级正确率】" + str(j['classScoreRate']) + "<br/>"
                        except:
                            errs += 1
                    if self.option[5][0] and not self.option[5][1]:
                        htmlTemp += "【解析】" + j['analysisHtml']
                    if self.option[6][0] and not self.option[6][1]:
                        htmlTemp += "【考察知识点】"
                        for kl in j['relatedKnowledgeGroups'][0]['relatedKnowledges']:
                            htmlTemp += kl['name'] + " "
                    htmlExport += htmlTemp + "<br/><hr/><br/>"
            htmlExport += "Generate By ZhiXueHacker. | Copyright © 2024-2025 HShiDianLu. All Rights Reserved."
            print("解析成功")
            print("正在生成文档")
            with open(self.exportPath + "/exportTemp.html", "w", encoding="utf-8") as f:
                f.write(htmlExport)
            pypandoc.convert_file(self.exportPath + "/exportTemp.html", 'docx',
                                  outputfile=self.exportPath + "/试卷.docx")
            os.remove(self.exportPath + "/exportTemp.html")
            print("生成成功")
            print("所有生成的文件均已保存至", self.exportPath)
            self.callback.emit(True, str(errs))
        except Exception as e:
            self.callback.emit(False, str(e))
            return


class FetchOnline(QThread):
    callback = pyqtSignal(bool, str, list, bool)

    def setPat(self, token, page):
        self.token = token
        self.page = page

    def run(self):
        try:
            s = requests.post("http://app.zhixue.com/api-onlineexam/onlineExamList/getOnlineExamPaperList",
                              data={"token": self.token, "status": 0, "pageIndex": self.page}).json()['result']
            print(s)
            if not s:
                self.callback.emit(True, "", [], 0)
            else:
                self.callback.emit(True, "", s['pageList'], s['totalPage'])
        except Exception as e:
            self.callback.emit(False, str(e), [], 0)


class FetchOnlineContent(QThread):
    callback = pyqtSignal(bool, str)
    problemListCallback = pyqtSignal(bool, str, list)
    countdownCallback = pyqtSignal(bool, str, int)

    def setPat(self, token, paperId):
        self.token = token
        self.paperId = paperId

    def run(self):
        try:
            s = requests.post("http://app.zhixue.com/api-onlineexam/onlineexam/getAttentionAndPaperStatus",
                              data={"token": self.token, "markingPaperId": self.paperId}).json()['result']
            print(s)
            self.callback.emit(True, s['attentionContent'])
        except Exception as e:
            self.callback.emit(False, str(e))
        try:
            s = requests.post("http://app.zhixue.com/api-onlineexam/onlineexam/gettopicandanswerlist",
                              data={"token": self.token, "markingPaperId": self.paperId}).json()['result']
            print(s)
            self.problemListCallback.emit(True, "", s)
        except Exception as e:
            self.problemListCallback.emit(False, str(e), [])
        try:
            s = requests.post(
                "http://app.zhixue.com/api-onlineexam/onlineExamList/getpapercountdown/?token=" + self.token + "&markingPaperId=" + self.paperId).json()[
                'result']
            print(s)
            self.countdownCallback.emit(True, "", s['countDown'])
        except Exception as e:
            self.countdownCallback.emit(False, str(e), -1)


class FetchProblem(QThread):
    callback = pyqtSignal(bool, str)

    def setPat(self, token, paperId, nums):
        self.token = token
        self.paperId = paperId
        self.nums = nums

    def run(self):
        try:
            params = urlencode({'token': self.token, 'markingPaperId': self.paperId, 'topicNums': [self.nums]})
            print(params)
            s = requests.post(
                "http://app.zhixue.com/api-onlineexam/onlineexam/getstemlist/?" + params).json()
            print(s)
            self.callback.emit(True, s['result'][0]['content'])
        except Exception as e:
            self.callback.emit(False, str(e))


class TickTimer(QThread):
    tick = pyqtSignal()

    def run(self):
        while True:
            time.sleep(1)
            self.tick.emit()


class TimeSyncer(QThread):
    value = pyqtSignal(bool, str, int)

    def setPat(self, token, paperId):
        self.token = token
        self.paperId = paperId

    def run(self):
        while True:
            time.sleep(60)
            if not (self.token and self.paperId):
                continue
            try:
                s = requests.post(
                    "http://app.zhixue.com/api-onlineexam/onlineExamList/getpapercountdown/?token=" + self.token + "&markingPaperId=" + self.paperId).json()[
                    'result']
                print(s)
                self.value.emit(True, "", s['countDown'])
            except Exception as e:
                self.value.emit(False, str(e), -1)


class TokenRefresher(QThread):
    errCallback = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.do = False

    def run(self):
        while True:
            time.sleep(600)
            if not self.do:
                continue
            try:
                if not os.path.exists(FILEDIR + "/cookies.json"):
                    continue
                with open(FILEDIR + "/cookies.json", "r", encoding="utf-8") as f:
                    cookies = json.load(f)
                for i in cookies:
                    if i['name'] == "JSESSIONID" and i['path'] == "/":
                        JSESSIONID = i['value']
                    if i['name'] == "tlsysSessionId":
                        tlsysSessionId = i['value']
                token = requests.get(url="https://www.zhixue.com/container/app/token/getToken",
                                     cookies={"JSESSIONID": JSESSIONID, "tlsysSessionId": tlsysSessionId}).json()
                print("Sync", token)
            except Exception as e:
                self.errCallback.emit(str(e))


def displayError(info):
    displayInfo = info.split("\n")
    if len(displayInfo) > 4:
        displayInfo = "\n".join(displayInfo[:4]) + "\n..."
    else:
        displayInfo = "\n".join(displayInfo)
        if (not "\n" in displayInfo) and len(displayInfo) > 200:
            displayInfo = displayInfo[:200] + "..."
        displayInfo = textwrap.fill(displayInfo, width=60)
    return displayInfo


class WebViewUi(FramelessWindow):
    loginFinishSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("WebView")
        self.resize(540, 335)
        # self.setTitleBar(CustomTitleBar(self))
        if isDarkTheme():
            self.setStyleSheet(DARKQSS)
        else:
            self.setStyleSheet(LIGHTQSS)
        ico_path = os.path.join(os.path.dirname(__file__), FILEDIR + "/ZhiXueIcon.ico")
        icon = QIcon()
        icon.addPixmap(QPixmap(ico_path), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(20, 32, 20, 15)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        self.widget = FramelessWebEngineView(self)
        self.widget.setStyleSheet("*{background: transparent}")
        self.widget.setMinimumSize(QSize(0, 169))
        self.widget.setObjectName("widget")
        self.gridLayout.addWidget(self.widget, 1, 0, 1, 3)
        self.PrimaryPushButton = PrimaryPushButton(self)
        self.PrimaryPushButton.setObjectName("PrimaryPushButton")
        self.gridLayout.addWidget(self.PrimaryPushButton, 3, 1, 1, 1)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        spacerItem2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)

        self.setWindowModality(Qt.ApplicationModal)
        self.PrimaryPushButton.clicked.connect(self.close)
        self.cookies = []
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.cookieAdd)
        self.widget.urlChanged.connect(self.urlChange)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "WebView"))
        self.PrimaryPushButton.setText(_translate("Form", "关闭"))

    def setup(self, url, width=540, height=335):
        print("setup")
        print(cfg.get(cfg.savePassword))
        if not cfg.get(cfg.savePassword):
            QWebEngineProfile.defaultProfile().cookieStore().deleteAllCookies()
        self.cookies = []
        self.widget.load(QUrl(url))
        self.resize(width, height)

    def cookieAdd(self, cookie):
        name = cookie.name().data().decode('utf-8')
        value = cookie.value().data().decode('utf-8')
        path = cookie.path()
        self.cookies.append({'name': name, 'value': value, 'path': path})
        print(name, path, value)

    def urlChange(self):
        if self.widget.url().url() == "https://www.zhixue.com/htm-vessel/#/":
            print("login end", self.cookies)
            self.close()
            with open(FILEDIR + "/cookies.json", "w", encoding="utf-8") as f:
                json.dump(self.cookies, f)
            print(self.cookies)
            if not cfg.get(cfg.savePassword):
                QWebEngineProfile.defaultProfile().cookieStore().deleteAllCookies()
            self.loginFinishSignal.emit()


class CookieBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('手动输入 Cookie', self)
        self.c1LineEdit = LineEdit(self)

        self.c1LineEdit.setPlaceholderText('tlsysSessionId')
        self.c1LineEdit.setClearButtonEnabled(True)

        self.c2LineEdit = LineEdit(self)

        self.c2LineEdit.setPlaceholderText('JSESSIONID')
        self.c2LineEdit.setClearButtonEnabled(True)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.c1LineEdit)
        self.viewLayout.addWidget(self.c2LineEdit)

        self.yesButton.setText('确定')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(600)


class MainUi(QFrame):
    mainSignal = pyqtSignal(list, int, list, int, dict, str)
    loginSignal = pyqtSignal(str, str)
    logoutSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("Main")
        # self.resize(750, 585)
        font = QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(10)
        self.setFont(font)
        # self.setStyleSheet("")
        self.gridLayout_2 = QGridLayout(self)
        self.gridLayout_2.setContentsMargins(20, 15 + windowOffset, 20, 15)
        self.gridLayout_2.setHorizontalSpacing(15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 4, 0, 1, 1)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.TitleLabel = TitleLabel(self)
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout_4.addWidget(self.TitleLabel)
        self.CaptionLabel = CaptionLabel(self)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.verticalLayout_4.addWidget(self.CaptionLabel)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 1, 0, 1, 2)
        spacerItem1 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 10, 0, 1, 2)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.StrongBodyLabel = StrongBodyLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.StrongBodyLabel.setFont(font)
        self.StrongBodyLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.verticalLayout_3.addWidget(self.StrongBodyLabel)
        self.CaptionLabel_2 = CaptionLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.CaptionLabel_2.setFont(font)
        self.CaptionLabel_2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.CaptionLabel_2.setObjectName("CaptionLabel_2")
        self.verticalLayout_3.addWidget(self.CaptionLabel_2)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 12, 0, 1, 2)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.StrongBodyLabel_2 = StrongBodyLabel(self)
        self.StrongBodyLabel_2.setObjectName("StrongBodyLabel_2")
        self.verticalLayout.addWidget(self.StrongBodyLabel_2)
        spacerItem2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.ListWidget = ListWidget(self)
        self.ListWidget.setObjectName("ListWidget")
        self.verticalLayout.addWidget(self.ListWidget)
        spacerItem3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.PrimaryPushButton_3 = PrimaryPushButton(self)
        self.PrimaryPushButton_3.setObjectName("PrimaryPushButton_3")
        self.horizontalLayout_5.addWidget(self.PrimaryPushButton_3)
        spacerItem4 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.PushButton_2 = PushButton(self)
        self.PushButton_2.setObjectName("PushButton_2")
        self.horizontalLayout_5.addWidget(self.PushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        spacerItem5 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem5)
        self.CaptionLabel_4 = CaptionLabel(self)
        self.CaptionLabel_4.setObjectName("CaptionLabel_4")
        self.verticalLayout.addWidget(self.CaptionLabel_4)
        self.gridLayout_2.addLayout(self.verticalLayout, 5, 0, 5, 1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.PrimaryPushButton = PrimaryPushButton(self)
        self.PrimaryPushButton.setObjectName("PrimaryPushButton")
        self.horizontalLayout.addWidget(self.PrimaryPushButton)
        spacerItem6 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.ToolButton = ToolButton(self)
        self.ToolButton.setObjectName("ToolButton")
        self.horizontalLayout.addWidget(self.ToolButton)
        spacerItem7 = QSpacerItem(30, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.CaptionLabel_3 = CaptionLabel(self)
        self.CaptionLabel_3.setObjectName("CaptionLabel_3")
        self.horizontalLayout.addWidget(self.CaptionLabel_3)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        spacerItem8 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem8, 2, 0, 1, 2)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.StrongBodyLabel_3 = StrongBodyLabel(self)
        self.StrongBodyLabel_3.setObjectName("StrongBodyLabel_3")
        self.verticalLayout_5.addWidget(self.StrongBodyLabel_3)
        spacerItem9 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem9)
        self.ListWidget_2 = ListWidget(self)
        self.ListWidget_2.setObjectName("ListWidget_2")
        self.verticalLayout_5.addWidget(self.ListWidget_2)
        spacerItem10 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem10)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.PrimaryPushButton_2 = PrimaryPushButton(self)
        self.PrimaryPushButton_2.setObjectName("PrimaryPushButton_2")
        self.horizontalLayout_2.addWidget(self.PrimaryPushButton_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout_5, 3, 1, 7, 1)
        spacerItem11 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem11, 11, 0, 1, 2)

        self.loginThread = LoginSelenium()
        self.loginThread.callback.connect(self.loginCallback)
        self.PrimaryPushButton.clicked.connect(self.login)
        self.getTokenThread = GetToken()
        self.getTokenThread.callback.connect(self.getTokenCallback)
        self.PrimaryPushButton.setEnabled(False)
        self.PrimaryPushButton_3.setEnabled(False)
        self.PushButton_2.setEnabled(False)
        self.PrimaryPushButton_2.setEnabled(False)
        self.ToolButton.setEnabled(False)
        self.fetchExamThread = FetchExam()
        self.fetchExamThread.callback.connect(self.fetchExamCallback)
        self.fetchPage = 1
        self.PushButton_2.clicked.connect(self.fetch)
        self.ListWidget.clicked.connect(lambda: self.PrimaryPushButton_3.setEnabled(True))
        self.fetchPaperThread = FetchPaper()
        self.fetchPaperThread.callback.connect(self.fetchPaperCallback)
        self.PrimaryPushButton_3.clicked.connect(self.selectExam)
        self.PrimaryPushButton_2.clicked.connect(self.fetchDetail)
        self.fetchRankThread = FetchRank()
        self.fetchRankThread.callback.connect(self.emitDetail)
        self.ListWidget_2.clicked.connect(lambda: self.PrimaryPushButton_2.setEnabled(True))
        self.ToolButton.clicked.connect(self.refresh)
        self.examList = []
        self.paperList = []
        self.examIndex = None
        self.subjectRank = None
        self.paperIndex = None
        self.username = None
        self.loginState = False
        self.ToolButton.setIcon(FIF.SYNC)
        self.tokenRefreshThread = TokenRefresher()
        self.tokenRefreshThread.errCallback.connect(self.tokenRefreshErr)
        self.tokenRefreshThread.start()
        self.paperDiffThread = PaperDiff()
        self.paperDiffThread.callback.connect(self.paperDiffCallback)
        self.paperDiffThread.setPat(None, None, None, None)
        self.paperDiffThread.start()
        self.newSubjectWindow = None
        self.firstTimeFetch = True

        if os.path.exists(FILEDIR + "/cookies.json"):
            self.getTokenThread.start()
        else:
            self.PrimaryPushButton.setEnabled(True)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "ZhiXueHacker"))
        self.PrimaryPushButton.setText(_translate("Form", "登录"))
        self.CaptionLabel_3.setText(_translate("Form", "未登录"))
        self.StrongBodyLabel.setText(_translate("Form", "Copyright © 2024-2025 HShiDianLu. All Rights Reserved."))
        self.CaptionLabel_2.setText(_translate("Form", "Version " + VERSION))
        self.StrongBodyLabel_2.setText(_translate("Form", "选择考试"))
        self.PrimaryPushButton_3.setText(_translate("Form", "选定该考试"))
        self.PushButton_2.setText(_translate("Form", "加载更多"))
        self.CaptionLabel_4.setText(_translate("Form", "注：由于智学网限制，一次性只能获取10次考试。"))
        self.TitleLabel.setText(_translate("Form", "ZhiXueHacker"))
        self.CaptionLabel.setText(_translate("Form", "智学网试卷 & 排名爬取工具"))
        self.StrongBodyLabel_3.setText(_translate("Form", "选择学科"))
        self.PrimaryPushButton_2.setText(_translate("Form", "查看详情"))

    def selectExam(self):
        self.examIndex = self.ListWidget.currentRow()
        self.ListWidget_2.clear()
        self.PrimaryPushButton_2.setEnabled(False)
        print(self.examList[self.examIndex]['examId'])
        self.fetchPaperThread.setPat(self.token, self.examList[self.examIndex]['examId'])
        self.fetchPaperThread.start()
        self.ListWidget_2.clearSelection()
        self.PrimaryPushButton_3.setEnabled(False)

    def logout(self, changeText):
        self.loginState = False
        if changeText:
            self.PrimaryPushButton.setText("登录")
            self.CaptionLabel_3.setText("未登录")
        self.ListWidget.clearSelection()
        self.ListWidget.clear()
        self.ListWidget_2.clearSelection()
        self.ListWidget_2.clear()
        self.PrimaryPushButton_3.setEnabled(False)
        self.PushButton_2.setEnabled(False)
        self.PrimaryPushButton_2.setEnabled(False)
        self.ToolButton.setEnabled(False)
        self.fetchPage = 1
        self.logoutSignal.emit()
        self.PushButton_2.setText("加载更多")
        self.tokenRefreshThread.do = False
        self.firstTimeFetch = True
        self.paperDiffThread.setPat(None, None, None, None)
        if self.newSubjectWindow:
            try:
                self.newSubjectWindow.close()
            except:
                pass

    def login(self):
        if not self.loginState:
            if cfg.get(cfg.loginMethod) == "Selenium":
                self.PrimaryPushButton.setEnabled(False)
                InfoBar.info(
                    title="登录",
                    content="请在打开的浏览器中完成登录。",
                    orient=Qt.Horizontal,
                    isClosable=False,
                    position=InfoBarPosition.BOTTOM,
                    duration=3000,
                    parent=self
                )
                self.loginThread.start()
            elif cfg.get(cfg.loginMethod) == "WebEngineView":
                InfoBar.info(
                    title="登录",
                    content="请在打开的窗口完成登录。",
                    orient=Qt.Horizontal,
                    isClosable=False,
                    position=InfoBarPosition.BOTTOM,
                    duration=3000,
                    parent=self
                )
                webView = WebViewUi()
                webView.setup("https://www.zhixue.com/login.html")
                webView.loginFinishSignal.connect(lambda: self.loginCallback(True, ""))
                webView.showMaximized()
            else:
                w = CookieBox(self)
                if w.exec():
                    if w.c1LineEdit.text() and w.c2LineEdit.text():
                        print(w.c1LineEdit.text(), w.c2LineEdit.text())
                        with open(FILEDIR + "/cookies.json", "w", encoding="utf-8") as f:
                            json.dump([{'name': 'tlsysSessionId', 'value': w.c1LineEdit.text(), 'path': '/'},
                                       {'name': 'JSESSIONID', 'value': w.c2LineEdit.text(), 'path': '/'}], f)
                        self.loginCallback(True, "")
        else:
            os.remove(FILEDIR + "/cookies.json")
            self.logout(True)
            InfoBar.success(
                title="退出登录成功",
                content="已清除 Cookie 并退出登录。",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=3000,
                parent=self
            )

    def fetch(self):
        self.PushButton_2.setEnabled(False)
        self.fetchPage += 1
        self.fetchExamThread.setPat(self.token, self.fetchPage)
        self.fetchExamThread.start()

    def fetchDetail(self):
        self.PrimaryPushButton_2.setEnabled(False)
        self.paperIndex = self.ListWidget_2.currentRow()
        self.fetchRankThread.setPat(self.token, self.examList[self.examIndex]['examId'],
                                    self.paperList[self.paperIndex]['paperId'],
                                    self.subjectRank, self.paperList[self.paperIndex]['subjectCode'], self.JSESSIONID,
                                    self.tlsysSessionId)
        self.fetchRankThread.start()

    def emitDetail(self, success, info, subjectRank):
        self.PrimaryPushButton_2.setEnabled(True)
        if success:
            self.mainSignal.emit(self.examList, self.examIndex, self.paperList, self.paperIndex, subjectRank,
                                 self.username)
        else:
            InfoBar.error(
                title="详情获取失败",
                content="错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )

    def refresh(self):
        self.ToolButton.setEnabled(False)
        self.PrimaryPushButton.setEnabled(False)
        self.logout(False)
        self.getTokenThread.start()

    def changeSyncState(self):
        self.tokenRefreshThread.do = cfg.get(cfg.autoSync)

    def tokenRefreshErr(self, info):
        InfoBar.error(
            title="Token 刷新失败",
            content="Token 可能已失效。\n" + "错误信息：" + displayError(info),
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.BOTTOM,
            duration=5000,
            parent=self
        )

    def loginCallback(self, success, info):
        if success:
            self.PrimaryPushButton.setEnabled(False)
            self.getTokenThread.start()
        else:
            self.PrimaryPushButton.setEnabled(True)
            InfoBar.error(
                title="登录失败",
                content="操作可能已被取消。\n错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )

    def getTokenCallback(self, success, JSESSIONID, tlsysSessionId, token, username):
        if success:
            self.JSESSIONID = JSESSIONID
            self.tlsysSessionId = tlsysSessionId
            self.token = token
            self.username = username
            self.CaptionLabel_3.setText("你好，" + self.username + "同学")
            self.loginSignal.emit(self.username, self.token)
            self.fetchExamThread.setPat(self.token, 1)
            self.fetchExamThread.start()
            self.ToolButton.setEnabled(True)
            InfoBar.success(
                title="登录成功",
                content="当前用户：" + self.username,
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=3000,
                parent=self
            )
            self.loginState = True
            self.PrimaryPushButton.setText("退出登录")
            self.changeSyncState()
        else:
            self.logout(True)
            InfoBar.error(
                title="登录失败",
                content="请重新登录。\n" + "错误信息：" + displayError(JSESSIONID),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )
        self.PrimaryPushButton.setEnabled(True)

    def fetchExamCallback(self, success, info, examTmpList, hasNext):
        if success:
            if not hasNext:
                self.PushButton_2.setText("没有更多了")
                self.PushButton_2.setEnabled(False)
            else:
                self.PushButton_2.setEnabled(True)
            for i in examTmpList:
                self.examList.append(i)
                self.ListWidget.addItem(QListWidgetItem(i['examName'] + " (" + i['examId'] + ")"))
            if self.firstTimeFetch:
                self.firstTimeFetch = False
                self.paperDiffThread.setPat(self.token, self.examList[0]['examId'], self.examList[0]['examName'], 0)
        else:
            InfoBar.error(
                title="考试列表获取失败",
                content="错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )
            self.PushButton_2.setEnabled(True)

    def fetchPaperCallback(self, success, info, paperList, subjectRank):
        self.PrimaryPushButton_3.setEnabled(True)
        if success:
            self.paperList = paperList
            self.subjectRank = subjectRank
            for i in paperList:
                self.ListWidget_2.addItem(
                    QListWidgetItem(i['subjectName'] + " (" + i['paperId'] + "-" + i['subjectCode'] + ")"))
            InfoBar.info(
                title="试卷获取成功",
                content="请在右侧选择试卷后查看详情。",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=3000,
                parent=self
            )
        else:
            InfoBar.error(
                title="试卷获取失败",
                content="错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )

    def autoSelectExam(self, row):
        self.ListWidget.setCurrentRow(row)
        self.selectExam()
        self.newSubjectWindow.close()

    def paperDiffCallback(self, success, info, newSubject, examName, rowId):
        if not cfg.get(cfg.newScoreMsg):
            return
        if success:
            if newSubject:
                self.newSubjectWindow = InfoBar(
                    icon=InfoBarIcon.INFORMATION,
                    title="成绩发布",
                    content=examName + "考试中的\n" + "、".join(newSubject) + "学科已出分。",
                    orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=-1,
                    parent=self
                )
                pb = PushButton("查看")
                self.newSubjectWindow.addWidget(pb)
                pb.clicked.connect(lambda: self.autoSelectExam(rowId))
                self.newSubjectWindow.show()
                tn = ToastNotifier()
                tn.show_toast("成绩发布", examName + "考试中的\n" + "、".join(newSubject) + "学科已出分。",
                              icon_path="./ZhiXueIcon.ico", duration=10, threaded=True)
        else:
            InfoBar.error(
                title="试卷获取失败",
                content="（成绩发布提醒）错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )


class DetailUi(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Detail")
        # self.resize(750, 585)
        font = QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(10)
        self.setFont(font)
        # self.setStyleSheet("")
        self.gridLayout_2 = QGridLayout(self)
        self.gridLayout_2.setContentsMargins(20, 15 + windowOffset, 20, 15)
        self.gridLayout_2.setHorizontalSpacing(15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 7, 0, 1, 2)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.StrongBodyLabel = StrongBodyLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.StrongBodyLabel.setFont(font)
        self.StrongBodyLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.verticalLayout_3.addWidget(self.StrongBodyLabel)
        self.CaptionLabel_2 = CaptionLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.CaptionLabel_2.setFont(font)
        self.CaptionLabel_2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.CaptionLabel_2.setObjectName("CaptionLabel_2")
        self.verticalLayout_3.addWidget(self.CaptionLabel_2)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 13, 0, 1, 2)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.StrongBodyLabel_3 = StrongBodyLabel(self)
        self.StrongBodyLabel_3.setObjectName("StrongBodyLabel_3")
        self.verticalLayout.addWidget(self.StrongBodyLabel_3)
        spacerItem1 = QSpacerItem(20, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.ListWidget_2 = ListWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ListWidget_2.sizePolicy().hasHeightForWidth())
        self.ListWidget_2.setSizePolicy(sizePolicy)
        self.ListWidget_2.setSelectionMode(QAbstractItemView.MultiSelection)
        self.ListWidget_2.setObjectName("ListWidget_2")
        self.verticalLayout.addWidget(self.ListWidget_2)
        spacerItem2 = QSpacerItem(20, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.PushButton = PushButton(self)
        self.PushButton.setObjectName("PushButton")
        self.horizontalLayout_2.addWidget(self.PushButton)
        spacerItem3 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.PushButton_3 = PushButton(self)
        self.PushButton_3.setObjectName("PushButton_3")
        self.horizontalLayout_2.addWidget(self.PushButton_3)
        spacerItem4 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.PrimaryPushButton_2 = PrimaryPushButton(self)
        self.PrimaryPushButton_2.setObjectName("PrimaryPushButton_2")
        self.horizontalLayout_2.addWidget(self.PrimaryPushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout, 8, 0, 2, 2)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.TitleLabel = TitleLabel(self)
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout_4.addWidget(self.TitleLabel)
        self.CaptionLabel = CaptionLabel(self)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.verticalLayout_4.addWidget(self.CaptionLabel)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.CaptionLabel_3 = CaptionLabel(self)
        self.CaptionLabel_3.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.CaptionLabel_3.setObjectName("CaptionLabel_3")
        self.gridLayout.addWidget(self.CaptionLabel_3, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 4, 0, 1, 2)
        spacerItem5 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem5, 5, 0, 1, 2)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.StrongBodyLabel_2 = StrongBodyLabel(self)
        self.StrongBodyLabel_2.setObjectName("StrongBodyLabel_2")
        self.verticalLayout_5.addWidget(self.StrongBodyLabel_2)
        spacerItem6 = QSpacerItem(20, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem6)
        self.ElevatedCardWidget = ElevatedCardWidget(self)
        self.ElevatedCardWidget.setObjectName("ElevatedCardWidget")
        self.verticalLayout_2 = QVBoxLayout(self.ElevatedCardWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.BodyLabel = BodyLabel(self.ElevatedCardWidget)
        self.BodyLabel.setObjectName("BodyLabel")
        self.verticalLayout_2.addWidget(self.BodyLabel)
        self.BodyLabel_2 = BodyLabel(self.ElevatedCardWidget)
        self.BodyLabel_2.setObjectName("BodyLabel_2")
        self.verticalLayout_2.addWidget(self.BodyLabel_2)
        self.BodyLabel_3 = BodyLabel(self.ElevatedCardWidget)
        self.BodyLabel_3.setObjectName("BodyLabel_3")
        self.verticalLayout_2.addWidget(self.BodyLabel_3)
        self.BodyLabel_4 = BodyLabel(self.ElevatedCardWidget)
        self.BodyLabel_4.setObjectName("BodyLabel_4")
        self.verticalLayout_2.addWidget(self.BodyLabel_4)
        self.BodyLabel_5 = BodyLabel(self.ElevatedCardWidget)
        self.BodyLabel_5.setObjectName("BodyLabel_5")
        self.verticalLayout_2.addWidget(self.BodyLabel_5)
        self.verticalLayout_5.addWidget(self.ElevatedCardWidget)
        self.gridLayout_2.addLayout(self.verticalLayout_5, 6, 0, 1, 2)
        spacerItem7 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem7, 12, 0, 1, 1)
        spacerItem8 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem8, 10, 0, 1, 1)

        self.examList = []
        self.paperList = []
        self.examIndex = None
        self.subjectRank = None
        self.paperIndex = None
        self.username = None
        self.problemList = None
        self.downloadPath = None
        self.PushButton.setEnabled(False)
        self.PushButton_3.setEnabled(False)
        self.PrimaryPushButton_2.setEnabled(False)
        self.PushButton.clicked.connect(self.selectAll)
        self.PushButton_3.clicked.connect(self.selectNone)
        self.ListWidget_2.clicked.connect(self.clickSheet)
        self.PrimaryPushButton_2.clicked.connect(self.download)
        self.downloadSheetThread = DownloadSheet()
        self.downloadSheetThread.callback.connect(self.downloadSheetCallback)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "ZhiXueHacker"))
        self.StrongBodyLabel_2.setText(_translate("Form", "科目详情"))
        self.StrongBodyLabel_3.setText(_translate("Form", "答题卡下载"))
        self.PushButton.setText(_translate("Form", "全选"))
        self.PushButton_3.setText(_translate("Form", "全不选"))
        self.PrimaryPushButton_2.setText(_translate("Form", "下载"))
        self.TitleLabel.setText(_translate("Form", "学科概览"))
        self.CaptionLabel.setText(_translate("Form", "当前考试：无 | 当前学科：无"))
        self.CaptionLabel_3.setText(_translate("Form", ""))
        self.StrongBodyLabel.setText(_translate("Form", "Copyright © 2024-2025 HShiDianLu. All Rights Reserved."))
        self.CaptionLabel_2.setText(_translate("Form", "Version " + VERSION))

    def activePage(self, examList, examIndex, paperList, paperIndex, subjectRank, username):
        self.examList = examList
        self.examIndex = examIndex
        self.paperList = paperList
        self.paperIndex = paperIndex
        self.subjectRank = subjectRank
        self.username = username
        self.CaptionLabel_3.setText(username + "同学")
        self.ListWidget_2.clearSelection()
        self.ListWidget_2.clear()
        self.PushButton.setEnabled(False)
        self.PushButton_3.setEnabled(False)
        self.PrimaryPushButton_2.setEnabled(False)
        print(self.paperIndex)
        self.CaptionLabel.setText(
            "当前考试：" + examList[examIndex]['examName'] + " | 当前学科：" + self.paperList[self.paperIndex][
                'subjectName'])
        self.downloadPath = cfg.get(cfg.exportFolder) + "/" + self.examList[self.examIndex]['examName'] + " - " + \
                            self.paperList[self.paperIndex]['subjectName']
        # self.BodyLabel.setText("学科：" + paperList[paperIndex]['subjectName'] + "\n\n"
        #                                                                         "ID：" + paperList[paperIndex][
        #                            'paperId'] + "-" + paperList[paperIndex]['subjectCode'] + "\n\n"
        #                                                                                      "分数：" + str(
        #     paperList[paperIndex]['userScore']) + "/" + str(paperList[paperIndex]['standardScore']) + "\n\n"
        #                                                                                               "参考人数（班级/学校）：" + str(
        #     subjectRank['classTotal']) + "/" + str(subjectRank['gradeTotal']) + "\n\n"
        #                                                                         "预计排名（班级）：" + str(
        #     subjectRank['rank']))
        self.BodyLabel.setText("学科：" + paperList[paperIndex]['subjectName'])
        self.BodyLabel_2.setText("ID：" + paperList[paperIndex]['paperId'] + "-" + paperList[paperIndex]['subjectCode'])
        self.BodyLabel_3.setText(
            "分数：" + str(paperList[paperIndex]['userScore']) + "/" + str(paperList[paperIndex]['standardScore']))
        self.BodyLabel_4.setText(
            "参考人数（班级/学校）：" + str(subjectRank['classTotal']) + "/" + str(subjectRank['gradeTotal']))
        if subjectRank['rank']:
            InfoBar.warning(
                title="排名功能警告",
                content="排名仅供参考，可能会有1名之差。具体请以教师端排名为准。",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )
            self.BodyLabel_5.setText("班级排名（预计）：" + str(subjectRank['rank']))
        else:
            InfoBar.error(
                title="排名获取失败",
                content="无法获取排名。这可能是由于试卷少于三科或学校未开启该功能。",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )
            self.BodyLabel_5.setText("班级排名（预计）：无")

    def logout(self):
        self.ListWidget_2.clearSelection()
        self.ListWidget_2.clear()
        self.examList = []
        self.paperList = []
        self.examIndex = None
        self.subjectRank = None
        self.paperIndex = None
        self.username = None
        self.PushButton.setEnabled(False)
        self.PushButton_3.setEnabled(False)
        self.PrimaryPushButton_2.setEnabled(False)
        self.problemList = None
        self.downloadPath = None
        self.BodyLabel.setText("")
        self.BodyLabel_2.setText("")
        self.BodyLabel_3.setText("")
        self.BodyLabel_4.setText("")
        self.BodyLabel_5.setText("")
        self.CaptionLabel.setText("当前考试：无 | 当前学科：无")
        self.CaptionLabel_3.setText("")

    def clickSheet(self):
        if len(self.ListWidget_2.selectedIndexes()) != 0:
            self.PrimaryPushButton_2.setEnabled(True)
        else:
            self.PrimaryPushButton_2.setEnabled(False)

    def selectAll(self):
        for i in range(self.ListWidget_2.count()):
            self.ListWidget_2.item(i).setSelected(True)
        self.PrimaryPushButton_2.setEnabled(True)

    def selectNone(self):
        self.ListWidget_2.clearSelection()
        self.PrimaryPushButton_2.setEnabled(False)

    def download(self):
        urls = []
        self.PrimaryPushButton_2.setEnabled(False)
        for i in self.ListWidget_2.selectedItems():
            urls.append(i.text())
        self.downloadSheetThread.setPat(self.downloadPath, urls)
        self.downloadSheetThread.start()

    def sheetCallback(self, success, info, sheetList):
        if success:
            for i in sheetList:
                self.ListWidget_2.addItem(QListWidgetItem(i))
            self.PushButton.setEnabled(True)
            self.PushButton_3.setEnabled(True)
        else:
            InfoBar.error(
                title="答题卡获取失败",
                content="错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )

    def downloadSheetCallback(self, success, info):
        self.PrimaryPushButton_2.setEnabled(True)
        if success:
            w = InfoBar(
                icon=InfoBarIcon.INFORMATION,
                title="下载成功",
                content="答题卡已保存至 " + self.downloadPath + " 目录下。",
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=-1,
                parent=self
            )
            pb = PushButton("打开文件夹")
            w.addWidget(pb)
            pb.clicked.connect(lambda link: QDesktopServices.openUrl(QUrl.fromLocalFile(self.downloadPath)))
            w.show()
        else:
            InfoBar.error(
                title="下载失败",
                content="错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )


class DownloadUI(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("Download")
        # self.resize(750, 599)
        font = QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(10)
        self.setFont(font)
        # self.setStyleSheet("")
        self.gridLayout_2 = QGridLayout(self)
        self.gridLayout_2.setContentsMargins(20, 15 + windowOffset, 20, 15)
        self.gridLayout_2.setHorizontalSpacing(15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 5, 0, 1, 2)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.StrongBodyLabel = StrongBodyLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.StrongBodyLabel.setFont(font)
        self.StrongBodyLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.verticalLayout_3.addWidget(self.StrongBodyLabel)
        self.CaptionLabel_2 = CaptionLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.CaptionLabel_2.setFont(font)
        self.CaptionLabel_2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.CaptionLabel_2.setObjectName("CaptionLabel_2")
        self.verticalLayout_3.addWidget(self.CaptionLabel_2)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 10, 0, 1, 2)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.TitleLabel = TitleLabel(self)
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout_4.addWidget(self.TitleLabel)
        self.CaptionLabel = CaptionLabel(self)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.verticalLayout_4.addWidget(self.CaptionLabel)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.CaptionLabel_3 = CaptionLabel(self)
        self.CaptionLabel_3.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.CaptionLabel_3.setObjectName("CaptionLabel_3")
        self.gridLayout.addWidget(self.CaptionLabel_3, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 4, 0, 1, 2)
        spacerItem1 = QSpacerItem(12, 21, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 8, 1, 1, 1)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.StrongBodyLabel_4 = StrongBodyLabel(self)
        self.StrongBodyLabel_4.setObjectName("StrongBodyLabel_4")
        self.verticalLayout_5.addWidget(self.StrongBodyLabel_4)
        spacerItem2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem2)
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.CheckBox_7 = CheckBox(self)
        self.CheckBox_7.setChecked(True)
        self.CheckBox_7.setObjectName("CheckBox_7")
        self.gridLayout_4.addWidget(self.CheckBox_7, 4, 0, 1, 1)
        self.SwitchButton_7 = SwitchButton(self)
        self.SwitchButton_7.setObjectName("SwitchButton_7")
        self.gridLayout_4.addWidget(self.SwitchButton_7, 6, 1, 1, 1)
        self.SwitchButton_4 = SwitchButton(self)
        self.SwitchButton_4.setObjectName("SwitchButton_4")
        self.gridLayout_4.addWidget(self.SwitchButton_4, 5, 1, 1, 1)
        self.SwitchButton_5 = SwitchButton(self)
        self.SwitchButton_5.setObjectName("SwitchButton_5")
        self.gridLayout_4.addWidget(self.SwitchButton_5, 7, 1, 1, 1)
        self.CheckBox_2 = CheckBox(self)
        self.CheckBox_2.setChecked(True)
        self.CheckBox_2.setObjectName("CheckBox_2")
        self.gridLayout_4.addWidget(self.CheckBox_2, 1, 0, 1, 1)
        self.SwitchButton_6 = SwitchButton(self)
        self.SwitchButton_6.setObjectName("SwitchButton_6")
        self.gridLayout_4.addWidget(self.SwitchButton_6, 8, 1, 1, 1)
        self.CheckBox = CheckBox(self)
        self.CheckBox.setChecked(True)
        self.CheckBox.setObjectName("CheckBox")
        self.gridLayout_4.addWidget(self.CheckBox, 2, 0, 1, 1)
        self.SwitchButton_3 = SwitchButton(self)
        self.SwitchButton_3.setObjectName("SwitchButton_3")
        self.gridLayout_4.addWidget(self.SwitchButton_3, 4, 1, 1, 1)
        self.CheckBox_8 = CheckBox(self)
        self.CheckBox_8.setChecked(True)
        self.CheckBox_8.setObjectName("CheckBox_8")
        self.gridLayout_4.addWidget(self.CheckBox_8, 8, 0, 1, 1)
        self.CheckBox_5 = CheckBox(self)
        self.CheckBox_5.setChecked(True)
        self.CheckBox_5.setObjectName("CheckBox_5")
        self.gridLayout_4.addWidget(self.CheckBox_5, 7, 0, 1, 1)
        self.CheckBox_3 = CheckBox(self)
        self.CheckBox_3.setEnabled(False)
        self.CheckBox_3.setChecked(True)
        self.CheckBox_3.setObjectName("CheckBox_3")
        self.gridLayout_4.addWidget(self.CheckBox_3, 3, 0, 1, 1)
        self.CheckBox_6 = CheckBox(self)
        self.CheckBox_6.setChecked(True)
        self.CheckBox_6.setObjectName("CheckBox_6")
        self.gridLayout_4.addWidget(self.CheckBox_6, 5, 0, 1, 1)
        self.CheckBox_4 = CheckBox(self)
        self.CheckBox_4.setChecked(True)
        self.CheckBox_4.setObjectName("CheckBox_4")
        self.gridLayout_4.addWidget(self.CheckBox_4, 6, 0, 1, 1)
        self.CaptionLabel_9 = CaptionLabel(self)
        self.CaptionLabel_9.setObjectName("CaptionLabel_9")
        self.gridLayout_4.addWidget(self.CaptionLabel_9, 0, 0, 1, 1)
        self.CaptionLabel_10 = CaptionLabel(self)
        self.CaptionLabel_10.setObjectName("CaptionLabel_10")
        self.gridLayout_4.addWidget(self.CaptionLabel_10, 0, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_4)
        self.CaptionLabel_6 = CaptionLabel(self)
        self.CaptionLabel_6.setObjectName("CaptionLabel_6")
        self.verticalLayout_5.addWidget(self.CaptionLabel_6)
        spacerItem3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem3)
        self.PrimaryPushButton = PrimaryPushButton(self)
        self.PrimaryPushButton.setObjectName("PrimaryPushButton")
        self.verticalLayout_5.addWidget(self.PrimaryPushButton)
        spacerItem4 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem4)
        self.IndeterminateProgressBar = IndeterminateProgressBar(self)
        self.IndeterminateProgressBar.setObjectName("IndeterminateProgressBar")
        self.verticalLayout_5.addWidget(self.IndeterminateProgressBar)
        self.gridLayout_2.addLayout(self.verticalLayout_5, 6, 0, 2, 2)

        self.examList = []
        self.paperList = []
        self.examIndex = None
        self.subjectRank = None
        self.paperIndex = None
        self.username = None
        self.problemList = None
        self.downloadPath = None
        self.PrimaryPushButton.setEnabled(False)
        self.IndeterminateProgressBar.stop()
        self.CheckBox.setChecked(True)
        self.CheckBox_2.setChecked(True)
        self.CheckBox_3.setChecked(True)
        self.CheckBox_4.setChecked(True)
        self.CheckBox_5.setChecked(True)
        self.CheckBox_6.setChecked(True)
        self.CheckBox_7.setChecked(True)
        self.CheckBox_8.setChecked(True)
        self.PrimaryPushButton.clicked.connect(self.generate)
        self.SwitchButton_3.setEnabled(False)
        self.SwitchButton_4.setEnabled(False)
        self.SwitchButton_5.setEnabled(False)
        self.SwitchButton_6.setEnabled(False)
        self.SwitchButton_7.setEnabled(False)
        self.generatePaperThread = GeneratePaper()
        self.generatePaperThread.callback.connect(self.generatePaperCallback)

        if not os.path.exists("pandoc.exe"):
            InfoBar.error(
                title="功能无法正常使用",
                content="无法找到 Pandoc。请尝试重新安装程序。",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=-1,
                parent=self
            )

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("", "ZhiXueHacker"))
        self.StrongBodyLabel.setText(_translate("Form", "Copyright © 2024-2025 HShiDianLu. All Rights Reserved."))
        self.CaptionLabel_2.setText(_translate("Form", "Version " + VERSION))
        self.TitleLabel.setText(_translate("Form", "试卷生成"))
        self.CaptionLabel.setText(_translate("Form", "当前考试：无 | 当前学科：无"))
        self.CaptionLabel_3.setText(_translate("Form", ""))
        self.StrongBodyLabel_4.setText(_translate("Form", "生成配置"))
        self.CheckBox_7.setText(_translate("Form", "原答案"))
        self.CheckBox_2.setText(_translate("Form", "得分"))
        self.CheckBox.setText(_translate("Form", "分值"))
        self.CheckBox_8.setText(_translate("Form", "考察知识点"))
        self.CheckBox_5.setText(_translate("Form", "解析"))
        self.CheckBox_3.setText(_translate("Form", "原题"))
        self.CheckBox_6.setText(_translate("Form", "正确答案"))
        self.CheckBox_4.setText(_translate("Form", "班级正确率"))
        self.CaptionLabel_9.setText(_translate("Form", "是否显示"))
        self.CaptionLabel_10.setText(_translate("Form", "是否置于文档末尾"))
        self.CaptionLabel_6.setText(_translate("Form",
                                               "注：顺序将自上而下排列。试卷必须入库才能生成，可能需要重新排版。"))
        self.PrimaryPushButton.setText(_translate("Form", "生成"))

        self.SwitchButton_3.setOnText("是")
        self.SwitchButton_3.setOffText("否")
        self.SwitchButton_4.setOnText("是")
        self.SwitchButton_4.setOffText("否")
        self.SwitchButton_5.setOnText("是")
        self.SwitchButton_5.setOffText("否")
        self.SwitchButton_6.setOnText("是")
        self.SwitchButton_6.setOffText("否")
        self.SwitchButton_7.setOnText("是")
        self.SwitchButton_7.setOffText("否")

        self.SwitchButton_3.setVisible(False)
        self.SwitchButton_4.setVisible(False)
        self.SwitchButton_5.setVisible(False)
        self.SwitchButton_6.setVisible(False)
        self.SwitchButton_7.setVisible(False)
        self.CaptionLabel_10.setVisible(False)

    def activePage(self, examList, examIndex, paperList, paperIndex, subjectRank, username):
        self.examList = examList
        self.examIndex = examIndex
        self.paperList = paperList
        self.paperIndex = paperIndex
        self.subjectRank = subjectRank
        self.username = username
        self.PrimaryPushButton.setEnabled(False)
        print(self.paperIndex)
        self.CaptionLabel.setText(
            "当前考试：" + examList[examIndex]['examName'] + " | 当前学科：" + self.paperList[self.paperIndex][
                'subjectName'])
        self.downloadPath = cfg.get(cfg.exportFolder) + "/" + self.examList[self.examIndex]['examName'] + " - " + \
                            self.paperList[self.paperIndex]['subjectName']

    def logout(self):
        self.examList = []
        self.paperList = []
        self.examIndex = None
        self.subjectRank = None
        self.paperIndex = None
        self.username = None
        self.problemList = None
        self.downloadPath = None
        self.PrimaryPushButton.setEnabled(False)
        self.IndeterminateProgressBar.stop()
        self.CheckBox.setChecked(True)
        self.CheckBox_2.setChecked(True)
        self.CheckBox_3.setChecked(True)
        self.CheckBox_4.setChecked(True)
        self.CheckBox_5.setChecked(True)
        self.CheckBox_6.setChecked(True)
        self.CheckBox_7.setChecked(True)
        self.CheckBox_8.setChecked(True)
        self.CaptionLabel.setText("当前考试：无 | 当前学科：无")

    def generate(self):
        self.PrimaryPushButton.setEnabled(False)
        self.generatePaperThread.setPat(self.downloadPath, self.problemList,
                                        "<h1>" + self.examList[self.examIndex]['examName'] + " (" +
                                        self.paperList[self.paperIndex][
                                            'subjectName'] + ")</h1>",
                                        [[self.CheckBox_2.isChecked(), False],
                                         [self.CheckBox.isChecked(), False],
                                         [self.CheckBox_7.isChecked(), self.SwitchButton_3.isChecked()],
                                         [self.CheckBox_6.isChecked(), self.SwitchButton_4.isChecked()],
                                         [self.CheckBox_4.isChecked(), self.SwitchButton_7.isChecked()],
                                         [self.CheckBox_5.isChecked(), self.SwitchButton_5.isChecked()],
                                         [self.CheckBox_8.isChecked(), self.SwitchButton_6.isChecked()]])
        self.generatePaperThread.start()
        InfoBar.info(
            title="生成试卷",
            content="正在生成试卷，这可能需要一定的时间。",
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.BOTTOM,
            duration=5000,
            parent=self
        )
        self.IndeterminateProgressBar.start()

    def generatePaperCallback(self, success, info):
        self.PrimaryPushButton.setEnabled(True)
        self.IndeterminateProgressBar.stop()
        if success:
            errmsg = "\n（共遇到 " + info + " 个错误，已自动跳过）"
            if info == "0":
                errmsg = ""
            w = InfoBar(
                icon=InfoBarIcon.INFORMATION,
                title="生成试卷成功",
                content="试卷已保存至 " + self.downloadPath + " 目录下。" + errmsg,
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=-1,
                parent=self
            )
            pb = PushButton("打开文件夹")
            w.addWidget(pb)
            pb.clicked.connect(lambda link: QDesktopServices.openUrl(QUrl.fromLocalFile(self.downloadPath)))
            w.show()
        else:
            InfoBar.error(
                title="生成试卷失败",
                content="错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )

    def problemCallback(self, success, info, problemList):
        if not os.path.exists("pandoc.exe"):
            return
        if success:
            self.problemList = problemList
            for i in self.problemList:
                for j in i['topicAnalysisDTOs']:
                    try:
                        print(j['disTitleNumber'])
                    except Exception as e:
                        InfoBar.error(
                            title="试卷解析失败",
                            content="无法解析试卷。这可能是由于试卷未入库。\n错误信息：" + displayError(str(e)),
                            orient=Qt.Horizontal,
                            isClosable=False,
                            position=InfoBarPosition.BOTTOM,
                            duration=5000,
                            parent=self
                        )
                        return
            self.PrimaryPushButton.setEnabled(True)
        else:
            InfoBar.error(
                title="试卷获取失败",
                content="错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )


class ScoreDetailUI(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("ScoreDetail")
        # self.resize(750, 585)
        font = QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(10)
        self.setFont(font)
        # self.setStyleSheet("")
        self.gridLayout_2 = QGridLayout(self)
        self.gridLayout_2.setContentsMargins(20, 15 + windowOffset, 20, 15)
        self.gridLayout_2.setHorizontalSpacing(15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.TreeWidget = TreeWidget(self)
        self.TreeWidget.setAnimated(True)
        self.TreeWidget.setWordWrap(True)
        self.TreeWidget.setObjectName("TreeWidget")
        self.TreeWidget.header().setVisible(True)
        self.TreeWidget.header().setCascadingSectionResizes(False)
        self.TreeWidget.header().setDefaultSectionSize(125)
        self.TreeWidget.header().setMinimumSectionSize(30)
        self.gridLayout_2.addWidget(self.TreeWidget, 6, 0, 1, 2)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.StrongBodyLabel = StrongBodyLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.StrongBodyLabel.setFont(font)
        self.StrongBodyLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.verticalLayout_3.addWidget(self.StrongBodyLabel)
        self.CaptionLabel_2 = CaptionLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.CaptionLabel_2.setFont(font)
        self.CaptionLabel_2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.CaptionLabel_2.setObjectName("CaptionLabel_2")
        self.verticalLayout_3.addWidget(self.CaptionLabel_2)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 9, 0, 1, 2)
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 7, 0, 1, 2)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.TitleLabel = TitleLabel(self)
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout_4.addWidget(self.TitleLabel)
        self.CaptionLabel = CaptionLabel(self)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.verticalLayout_4.addWidget(self.CaptionLabel)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.CaptionLabel_3 = CaptionLabel(self)
        self.CaptionLabel_3.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.CaptionLabel_3.setObjectName("CaptionLabel_3")
        self.gridLayout.addWidget(self.CaptionLabel_3, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 4, 0, 1, 2)
        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 5, 0, 1, 2)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "ZhiXueHacker"))
        self.StrongBodyLabel.setText(_translate("Form", "Copyright © 2024-2025 HShiDianLu. All Rights Reserved."))
        self.CaptionLabel_2.setText(_translate("Form", "Version " + VERSION))
        self.TitleLabel.setText(_translate("Form", "得分详情"))
        self.CaptionLabel.setText(_translate("Form", "当前考试：无 | 当前学科：无"))
        self.CaptionLabel_3.setText(_translate("Form", ""))
        self.TreeWidget.headerItem().setText(0, _translate("Form", "题号"))
        self.TreeWidget.headerItem().setText(1, _translate("Form", "得分"))
        self.TreeWidget.headerItem().setText(2, _translate("Form", "评分方式"))
        self.TreeWidget.headerItem().setText(3, _translate("Form", "批阅教师"))
        self.TreeWidget.headerItem().setText(4, _translate("Form", "批阅时间"))
        __sortingEnabled = self.TreeWidget.isSortingEnabled()
        self.TreeWidget.setSortingEnabled(__sortingEnabled)

    def activePage(self, examList, examIndex, paperList, paperIndex, subjectRank, username):
        self.examList = examList
        self.examIndex = examIndex
        self.paperList = paperList
        self.paperIndex = paperIndex
        self.subjectRank = subjectRank
        self.username = username
        self.CaptionLabel_3.setText(username + "同学")
        self.TreeWidget.clearSelection()
        self.TreeWidget.clear()
        print(self.paperIndex)
        self.CaptionLabel.setText(
            "当前考试：" + examList[examIndex]['examName'] + " | 当前学科：" + self.paperList[self.paperIndex][
                'subjectName'])
        self.downloadPath = cfg.get(cfg.exportFolder) + "/" + self.examList[self.examIndex]['examName'] + " - " + \
                            self.paperList[self.paperIndex]['subjectName']

    def logout(self):
        self.TreeWidget.clearSelection()
        self.TreeWidget.clear()
        self.examList = []
        self.paperList = []
        self.examIndex = None
        self.subjectRank = None
        self.paperIndex = None
        self.username = None
        self.problemList = None
        self.downloadPath = None
        self.CaptionLabel.setText("当前考试：无 | 当前学科：无")
        self.CaptionLabel_3.setText("")

    def scoreDetailCallback(self, success, info, scoreList):
        if success:
            print(scoreList)
            for i in scoreList:
                root = QTreeWidgetItem(self.TreeWidget)
                root.setText(0, i['dispTitle'])
                root.setText(1, str(i['score']) + "/" + str(i['standardScore']))
                try:
                    for j in i['subTopics']:
                        if j['subTopicIndex'] == -1:
                            if len(j['teacherMarkingRecords']) != 1:
                                if "marking" in j['scoreSource']:
                                    root.setText(2, "取" + ROLES[
                                        int(j['scoreSource'].replace("marking", "")) - 1] + "分数")
                                elif j['scoreSource'] == "average":
                                    root.setText(2, "取平均分数")
                                else:
                                    root.setText(2, "取" + j['scoreSource'] + "分数")
                                for k in j['teacherMarkingRecords']:
                                    sub = QTreeWidgetItem(root)
                                    if "marking" in k['role']:
                                        sub.setText(0, ROLES[int(k['role'].replace("marking", "")) - 1])
                                    else:
                                        sub.setText(0, k['role'])
                                    sub.setText(1, str(k['score']))
                                    sub.setText(3, k['teacherName'])
                                    sub.setText(4,
                                                time.strftime("%Y-%m-%d %H:%M:%S",
                                                              time.localtime(k['markingTime'] / 1000)))
                                    root.addChild(sub)
                            else:
                                root.setText(3, j['teacherMarkingRecords'][0]['teacherName'])
                                root.setText(4, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                                    j['teacherMarkingRecords'][0]['markingTime'] / 1000)))
                        else:
                            sub = QTreeWidgetItem(root)
                            sub.setText(0, i['dispTitle'] + "." + str(j['subTopicIndex']))
                            sub.setText(1, str(j['score']))
                            if len(j['teacherMarkingRecords']) != 1:
                                if "marking" in j['scoreSource']:
                                    sub.setText(2,
                                                "取" + ROLES[int(j['scoreSource'].replace("marking", "")) - 1] + "分数")
                                elif j['scoreSource'] == "average":
                                    sub.setText(2, "取平均分数")
                                else:
                                    sub.setText(2, "取" + j['scoreSource'] + "分数")
                                for k in j['teacherMarkingRecords']:
                                    teacher = QTreeWidgetItem(sub)
                                    if "marking" in k['role']:
                                        teacher.setText(0, ROLES[int(k['role'].replace("marking", "")) - 1])
                                    else:
                                        teacher.setText(0, k['role'])
                                    teacher.setText(1, str(k['score']))
                                    teacher.setText(3, k['teacherName'])
                                    teacher.setText(4,
                                                    time.strftime("%Y-%m-%d %H:%M:%S",
                                                                  time.localtime(k['markingTime'] / 1000)))
                                    root.addChild(teacher)
                                root.addChild(sub)
                            else:
                                sub.setText(3, j['teacherMarkingRecords'][0]['teacherName'])
                                sub.setText(4, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                                    j['teacherMarkingRecords'][0]['markingTime'] / 1000)))
                except Exception as e:
                    print(e)
            self.TreeWidget.expandAll()
        else:
            InfoBar.error(
                title="得分详情获取失败",
                content="错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )


class SettingUi(QFrame):
    syncChange = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("Setting")
        # self.resize(750, 585)
        font = QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(10)
        self.setFont(font)
        # self.setStyleSheet("")
        self.gridLayout_2 = QGridLayout(self)
        self.gridLayout_2.setContentsMargins(20, 15 + windowOffset, 0, 15)
        self.gridLayout_2.setHorizontalSpacing(70)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.TitleLabel = TitleLabel(self)
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout_4.addWidget(self.TitleLabel)
        self.CaptionLabel = CaptionLabel(self)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.verticalLayout_4.addWidget(self.CaptionLabel)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 1, 0, 1, 2)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.StrongBodyLabel = StrongBodyLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.StrongBodyLabel.setFont(font)
        self.StrongBodyLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.verticalLayout_3.addWidget(self.StrongBodyLabel)
        self.CaptionLabel_2 = CaptionLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.CaptionLabel_2.setFont(font)
        self.CaptionLabel_2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.CaptionLabel_2.setObjectName("CaptionLabel_2")
        self.verticalLayout_3.addWidget(self.CaptionLabel_2)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 5, 0, 1, 2)
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 2)
        spacerItem1 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 4, 0, 1, 1)
        # self.verticalLayout = QVBoxLayout()
        # self.verticalLayout.setObjectName("verticalLayout")
        # spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.verticalLayout.addItem(spacerItem2)
        self.settingCardsWidget = SettingCards()
        self.gridLayout_2.addWidget(self.settingCardsWidget, 3, 0, 1, 2)
        self.settingCardsWidget.exportCard.clicked.connect(self.changeDir)
        self.settingCardsWidget.syncCard.checkedChanged.connect(self.syncChange.emit)
        cfg.appRestartSig.connect(self.showRestart)
        self.showState = False

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "ZhiXueHacker"))
        self.TitleLabel.setText(_translate("Form", "设置"))
        self.CaptionLabel.setText(_translate("Form", "设置程序运行方式"))
        self.StrongBodyLabel.setText(_translate("Form", "Copyright © 2024-2025 HShiDianLu. All Rights Reserved."))
        self.CaptionLabel_2.setText(_translate("Form", "Version " + VERSION))

    def changeDir(self):
        file = QFileDialog.getExistingDirectory(self, "请选择下载文件夹")
        if file:
            cfg.set(cfg.exportFolder, file)
            self.exportCard.setContent(file)

    def showRestart(self):
        if not self.showState:
            InfoBar.warning(
                title="需要重启",
                content="需要重新启动程序以应用更改。",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=-1,
                parent=self
            )
            self.showState = True


class SettingCards(ScrollArea):
    def __init__(self):
        super().__init__()
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(0, 0, 20, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 0)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setStyleSheet("*{background:transparent !important;border:none;}")
        self.mainGroup = SettingCardGroup("系统", self.scrollWidget)
        self.exportCard = PushSettingCard(
            text="选择文件夹",
            icon=FIF.DOWNLOAD,
            title="下载文件夹",
            content=cfg.get(cfg.exportFolder)
        )
        self.mainGroup.addSettingCard(self.exportCard)
        self.syncCard = SwitchSettingCard(
            configItem=cfg.autoSync,
            icon=FIF.SYNC,
            title="自动刷新",
            content="每隔10分钟自动刷新用户以防止 Session 过期"
        )
        self.mainGroup.addSettingCard(self.syncCard)
        # self.saveCard = SwitchSettingCard(
        #     configItem=cfg.savePassword,
        #     icon=FIF.SAVE,
        #     title="保存密码",
        #     content="自动保存上一次成功登录的用户名和密码以在下次登录时自动填入（不建议在公共场所开启）"
        # )
        # self.mainGroup.addSettingCard(self.saveCard)
        self.msgCard = SwitchSettingCard(
            configItem=cfg.newScoreMsg,
            icon=FIF.RINGER,
            title="成绩发布提醒",
            content="有新成绩发布时自动提醒"
        )
        self.mainGroup.addSettingCard(self.msgCard)

        self.otherGroup = SettingCardGroup("个性化", self.scrollWidget)
        self.themeCard = OptionsSettingCard(
            configItem=cfg.theme,
            icon=FIF.BRUSH,
            title="主题",
            content="调整应用外观",
            texts=["浅色", "深色", "跟随系统设置"]
        )
        self.otherGroup.addSettingCard(self.themeCard)
        self.micaCard = SwitchSettingCard(
            configItem=cfg.mica,
            icon=FIF.TRANSPARENT,
            title="云母效果",
            content="窗口显示半透明"
        )
        self.otherGroup.addSettingCard(self.micaCard)

        self.advGroup = SettingCardGroup("高级", self.scrollWidget)
        self.loginCard = ComboBoxSettingCard(
            configItem=cfg.loginMethod,
            icon=FIF.GLOBE,
            title="登录方式",
            content="选择登录账户时采用的方式（若 WebEngineView 经常崩溃，请更换为 Selenium）",
            texts=["WebEngineView", "Selenium", "手动填入 Cookie"]
        )
        self.advGroup.addSettingCard(self.loginCard)
        self.renderCard = ComboBoxSettingCard(
            configItem=cfg.renderMethod,
            icon=FIF.VIEW,
            title="渲染方式",
            content="可缓解由于兼容性导致的 WebEngineView 崩溃问题",
            texts=["DesktopOpenGL", "OpenGLES", "SoftwareOpenGL"]
        )
        self.advGroup.addSettingCard(self.renderCard)

        self.expandLayout.addWidget(self.mainGroup)
        self.expandLayout.addWidget(self.otherGroup)
        self.expandLayout.addWidget(self.advGroup)


class InfoUi(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("Info")
        # self.resize(723, 585)
        font = QFont()
        font.setFamily("DengXian")
        font.setPointSize(10)
        self.setFont(font)
        # self.setStyleSheet("")
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(20, 15 + windowOffset, 20, 15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.TitleLabel = TitleLabel(self)
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout_2.addWidget(self.TitleLabel)
        self.CaptionLabel = CaptionLabel(self)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.verticalLayout_2.addWidget(self.CaptionLabel)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.BodyLabel = BodyLabel(self)
        self.BodyLabel.setObjectName("BodyLabel")
        self.verticalLayout.addWidget(self.BodyLabel)
        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.ElevatedCardWidget = ElevatedCardWidget(self)
        self.ElevatedCardWidget.setObjectName("ElevatedCardWidget")
        self.verticalLayout_3 = QVBoxLayout(self.ElevatedCardWidget)
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.StrongBodyLabel_3 = StrongBodyLabel(self.ElevatedCardWidget)
        self.StrongBodyLabel_3.setObjectName("StrongBodyLabel_3")
        self.verticalLayout_3.addWidget(self.StrongBodyLabel_3)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.BodyLabel_3 = BodyLabel(self.ElevatedCardWidget)
        self.BodyLabel_3.setObjectName("BodyLabel_3")
        self.verticalLayout_6.addWidget(self.BodyLabel_3)
        self.BodyLabel_5 = BodyLabel(self.ElevatedCardWidget)
        self.BodyLabel_5.setObjectName("BodyLabel_5")
        self.verticalLayout_6.addWidget(self.BodyLabel_5)
        self.verticalLayout_3.addLayout(self.verticalLayout_6)
        self.verticalLayout.addWidget(self.ElevatedCardWidget)
        spacerItem2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.ElevatedCardWidget_3 = ElevatedCardWidget(self)
        self.ElevatedCardWidget_3.setObjectName("ElevatedCardWidget_3")
        self.gridLayout_2 = QGridLayout(self.ElevatedCardWidget_3)
        self.gridLayout_2.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.BodyLabel_10 = BodyLabel(self.ElevatedCardWidget_3)
        self.BodyLabel_10.setObjectName("BodyLabel_10")
        self.gridLayout_2.addWidget(self.BodyLabel_10, 2, 1, 3, 1)
        self.CaptionLabel_2 = CaptionLabel(self.ElevatedCardWidget_3)
        self.CaptionLabel_2.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.CaptionLabel_2.setObjectName("CaptionLabel_2")
        self.gridLayout_2.addWidget(self.CaptionLabel_2, 2, 2, 1, 1)
        self.StrongBodyLabel_6 = StrongBodyLabel(self.ElevatedCardWidget_3)
        self.StrongBodyLabel_6.setObjectName("StrongBodyLabel_6")
        self.gridLayout_2.addWidget(self.StrongBodyLabel_6, 0, 0, 1, 2)
        self.ToolButton_2 = ToolButton(self.ElevatedCardWidget_3)
        self.ToolButton_2.setObjectName("ToolButton_2")
        self.ToolButton_2.setIcon(FIF.GITHUB)
        self.gridLayout_2.addWidget(self.ToolButton_2, 2, 0, 3, 1)
        self.CaptionLabel_3 = CaptionLabel(self.ElevatedCardWidget_3)
        self.CaptionLabel_3.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.CaptionLabel_3.setObjectName("CaptionLabel_3")
        self.gridLayout_2.addWidget(self.CaptionLabel_3, 3, 2, 1, 1)
        spacerItem3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem3, 1, 0, 1, 3)
        self.verticalLayout.addWidget(self.ElevatedCardWidget_3)
        spacerItem4 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem4)
        self.ElevatedCardWidget_2 = ElevatedCardWidget(self)
        self.ElevatedCardWidget_2.setObjectName("ElevatedCardWidget_2")
        self.verticalLayout_4 = QVBoxLayout(self.ElevatedCardWidget_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.StrongBodyLabel = StrongBodyLabel(self.ElevatedCardWidget_2)
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.verticalLayout_4.addWidget(self.StrongBodyLabel)
        self.PlainTextEdit = PlainTextEdit(self.ElevatedCardWidget_2)
        self.PlainTextEdit.setReadOnly(True)
        self.PlainTextEdit.setObjectName("PlainTextEdit")
        self.verticalLayout_4.addWidget(self.PlainTextEdit)
        self.verticalLayout.addWidget(self.ElevatedCardWidget_2)
        spacerItem5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)

        self.ToolButton_2.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://github.com/HShiDianLu/ZhiXueHacker")))

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "ZhiXueHacker"))
        self.TitleLabel.setText(_translate("Form", "关于"))
        self.CaptionLabel.setText(_translate("Form", "ZhiXueHacker"))
        self.BodyLabel.setText(
            _translate("Form", "ZhiXueHacker 是一款可以获取考试分数、排名（预测）、试卷、答题卡及进行在线考试的工具。"))
        self.StrongBodyLabel_3.setText(_translate("Form", "程序信息"))
        self.BodyLabel_3.setText(_translate("Form", "Author: HShiDianLu."))
        self.BodyLabel_5.setText(_translate("Form", "Version: " + VERSION))
        self.BodyLabel_10.setText(_translate("Form", "Github"))
        self.CaptionLabel_2.setText(_translate("Form", "Licensed under The MIT License"))
        self.StrongBodyLabel_6.setText(_translate("Form", "开源"))
        self.CaptionLabel_3.setText(_translate("Form", "Copyright © 2024-2025 HShiDianLu. All Rights Reserved."))
        self.StrongBodyLabel.setText(_translate("Form", "Pandoc License"))
        self.PlainTextEdit.setPlainText(_translate("Form", "Pandoc\n"
                                                           "Copyright (C) 2006-2023 John MacFarlane <jgm at berkeley dot edu>\n"
                                                           "\n"
                                                           "With the exceptions noted below, this code is released under the [GPL],\n"
                                                           "version 2 or later:\n"
                                                           "\n"
                                                           "   This program is free software; you can redistribute it and/or modify\n"
                                                           "   it under the terms of the GNU General Public License as published by\n"
                                                           "   the Free Software Foundation; either version 2 of the License, or\n"
                                                           "   (at your option) any later version.\n"
                                                           "\n"
                                                           "   This program is distributed in the hope that it will be useful,\n"
                                                           "   but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
                                                           "   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
                                                           "   GNU General Public License for more details.\n"
                                                           "\n"
                                                           "   You should have received a copy of the GNU General Public License\n"
                                                           "   along with this program; if not, write to the Free Software\n"
                                                           "   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA\n"
                                                           "\n"
                                                           "The GNU General Public License is available in the file COPYING.md in\n"
                                                           "the source distribution.  On Debian systems, the complete text of the\n"
                                                           "GPL can be found in `/usr/share/common-licenses/GPL`.\n"
                                                           "\n"
                                                           "[GPL]: https://www.gnu.org/copyleft/gpl.html\n"
                                                           "\n"
                                                           "Pandoc\'s complete source code is available from the [Pandoc home page].\n"
                                                           "\n"
                                                           "[Pandoc home page]: https://pandoc.org\n"
                                                           "\n"
                                                           "Pandoc includes some code with different copyrights, or subject to different\n"
                                                           "licenses.  The copyright and license statements for these sources are included\n"
                                                           "below.  All are GPL-compatible licenses.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "The modules in the `pandoc-types` repository (Text.Pandoc.Definition,\n"
                                                           "Text.Pandoc.Builder, Text.Pandoc.Generics, Text.Pandoc.JSON,\n"
                                                           "Text.Pandoc.Walk) are licensed under the BSD 3-clause license:\n"
                                                           "\n"
                                                           "Copyright (c) 2006-2023, John MacFarlane\n"
                                                           "\n"
                                                           "All rights reserved.\n"
                                                           "\n"
                                                           "Redistribution and use in source and binary forms, with or without\n"
                                                           "modification, are permitted provided that the following conditions are met:\n"
                                                           "\n"
                                                           "    * Redistributions of source code must retain the above copyright\n"
                                                           "      notice, this list of conditions and the following disclaimer.\n"
                                                           "\n"
                                                           "    * Redistributions in binary form must reproduce the above\n"
                                                           "      copyright notice, this list of conditions and the following\n"
                                                           "      disclaimer in the documentation and/or other materials provided\n"
                                                           "      with the distribution.\n"
                                                           "\n"
                                                           "    * Neither the name of John MacFarlane nor the names of other\n"
                                                           "      contributors may be used to endorse or promote products derived\n"
                                                           "      from this software without specific prior written permission.\n"
                                                           "\n"
                                                           "THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS\n"
                                                           "\"AS IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT\n"
                                                           "LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR\n"
                                                           "A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT\n"
                                                           "OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,\n"
                                                           "SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT\n"
                                                           "LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,\n"
                                                           "DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY\n"
                                                           "THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n"
                                                           "(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE\n"
                                                           "OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "Pandoc\'s templates (in `data/templates`) are dual-licensed as either\n"
                                                           "GPL (v2 or higher, same as pandoc) or (at your option) the BSD\n"
                                                           "3-clause license.\n"
                                                           "\n"
                                                           "Copyright (c) 2014--2023, John MacFarlane\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "src/Text/Pandoc/Writers/Muse.hs\n"
                                                           "Copyright (C) 2017-2020 Alexander Krotov\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "src/Text/Pandoc/Writers/Texinfo.hs\n"
                                                           "Copyright (C) 2008-2023 John MacFarlane and Peter Wang\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "src/Text/Pandoc/Writers/OpenDocument.hs\n"
                                                           "Copyright (C) 2008-2023 Andrea Rossato and John MacFarlane\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "src/Text/Pandoc/Writers/Org.hs\n"
                                                           "Copyright (C) 2010-2023 Puneeth Chaganti, John MacFarlane, and\n"
                                                           "                        Albert Krewinkel\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "src/Text/Pandoc/Writers/ZimWiki.hs\n"
                                                           "Copyright (C) 2017 Alex Ivkin\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "src/Text/Pandoc/Readers/Docx.hs\n"
                                                           "src/Text/Pandoc/Readers/Docx/*\n"
                                                           "Copyright (C) 2014-2020 Jesse Rosenthal\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "src/Text/Pandoc/Readers/Textile.hs\n"
                                                           "Copyright (C) 2010-2023 Paul Rivier and John MacFarlane\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "src/Text/Pandoc/Readers/TikiWiki.hs\n"
                                                           "Copyright (C) 2017 Robin Lee Powell\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "src/Text/Pandoc/Readers/JATS.hs\n"
                                                           "Copyright (C) 2017-2018 Hamish Mackenzie\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "src/Text/Pandoc/Readers/EPUB.hs\n"
                                                           "Copyright (C) 2014-2023 Matthew Pickering and John MacFarlane\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "src/Text/Pandoc/Readers/Org.hs\n"
                                                           "src/Text/Pandoc/Readers/Org/*\n"
                                                           "test/Tests/Readers/Org/*\n"
                                                           "Copyright (C) 2014-2023 Albert Krewinkel\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "pandoc-lua-engine/src/Text/Pandoc/Lua.hs\n"
                                                           "pandoc-lua-engine/src/Text/Pandoc/Lua/*\n"
                                                           "pandoc-lua-engine/test/lua/*\n"
                                                           "Copyright (C) 2017--2023 Albert Krewinkel and John MacFarlane\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "src/Text/Pandoc/Readers/Jira.hs\n"
                                                           "src/Text/Pandoc/Writers/Jira.hs\n"
                                                           "test/Tests/Readers/Jira.hs\n"
                                                           "Copyright (C) 2019--2023 Albert Krewinkel\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "src/Text/Pandoc/Readers/FB2.hs\n"
                                                           "Copyright (C) 2018--2019 Alexander Krotov\n"
                                                           "\n"
                                                           "Released under the GNU General Public License version 2 or later.\n"
                                                           "\n"
                                                           "----------------------------------------------------------------------\n"
                                                           "The dzslides template contains JavaScript and CSS from Paul Rouget\'s\n"
                                                           "dzslides template.\n"
                                                           "https://github.com/paulrouget/dzslides\n"
                                                           "\n"
                                                           "Released under the Do What the Fuck You Want To Public License.\n"
                                                           "\n"
                                                           "------------------------------------------------------------------------\n"
                                                           "Pandoc embeds a Lua interpreter (via hslua).\n"
                                                           "\n"
                                                           "Copyright © 1994–2022 Lua.org, PUC-Rio.\n"
                                                           "\n"
                                                           "Permission is hereby granted, free of charge, to any person obtaining\n"
                                                           "a copy of this software and associated documentation files (the\n"
                                                           "\"Software\"), to deal in the Software without restriction, including\n"
                                                           "without limitation the rights to use, copy, modify, merge, publish,\n"
                                                           "distribute, sublicense, and/or sell copies of the Software, and to\n"
                                                           "permit persons to whom the Software is furnished to do so, subject to\n"
                                                           "the following conditions:\n"
                                                           "\n"
                                                           "The above copyright notice and this permission notice shall be\n"
                                                           "included in all copies or substantial portions of the Software.\n"
                                                           "\n"
                                                           "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND,\n"
                                                           "EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\n"
                                                           "MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND\n"
                                                           "NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE\n"
                                                           "LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION\n"
                                                           "OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION\n"
                                                           "WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."))


class ExamListUi(QFrame):
    examSignal = pyqtSignal(str, str, str, int)
    examSwitchSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("ExamList")
        # self.resize(750, 599)
        font = QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(10)
        self.setFont(font)
        # self.setStyleSheet("")
        self.gridLayout_2 = QGridLayout(self)
        self.gridLayout_2.setContentsMargins(20, 15 + windowOffset, 20, 15)
        self.gridLayout_2.setHorizontalSpacing(15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.CaptionLabel_3 = CaptionLabel(self)
        self.CaptionLabel_3.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.CaptionLabel_3.setObjectName("CaptionLabel_3")
        self.gridLayout.addWidget(self.CaptionLabel_3, 1, 1, 1, 1)
        self.TitleLabel = TitleLabel(self)
        self.TitleLabel.setObjectName("TitleLabel")
        self.gridLayout.addWidget(self.TitleLabel, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 2)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.StrongBodyLabel = StrongBodyLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.StrongBodyLabel.setFont(font)
        self.StrongBodyLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.verticalLayout_3.addWidget(self.StrongBodyLabel)
        self.CaptionLabel_2 = CaptionLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.CaptionLabel_2.setFont(font)
        self.CaptionLabel_2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.CaptionLabel_2.setObjectName("CaptionLabel_2")
        self.verticalLayout_3.addWidget(self.CaptionLabel_2)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 5, 0, 1, 2)
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 4, 0, 1, 2)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.StrongBodyLabel_3 = StrongBodyLabel(self)
        self.StrongBodyLabel_3.setObjectName("StrongBodyLabel_3")
        self.verticalLayout_5.addWidget(self.StrongBodyLabel_3)
        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem1)
        self.ElevatedCardWidget = ElevatedCardWidget(self)
        self.ElevatedCardWidget.setObjectName("ElevatedCardWidget")
        self.verticalLayout_6 = QVBoxLayout(self.ElevatedCardWidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.BodyLabel = BodyLabel(self.ElevatedCardWidget)
        self.BodyLabel.setObjectName("BodyLabel")
        self.verticalLayout_6.addWidget(self.BodyLabel)
        self.BodyLabel_3 = BodyLabel(self.ElevatedCardWidget)
        self.BodyLabel_3.setObjectName("BodyLabel_3")
        self.verticalLayout_6.addWidget(self.BodyLabel_3)
        self.BodyLabel_4 = BodyLabel(self.ElevatedCardWidget)
        self.BodyLabel_4.setObjectName("BodyLabel_4")
        self.verticalLayout_6.addWidget(self.BodyLabel_4)
        self.BodyLabel_2 = BodyLabel(self.ElevatedCardWidget)
        self.BodyLabel_2.setObjectName("BodyLabel_2")
        self.verticalLayout_6.addWidget(self.BodyLabel_2)
        self.BodyLabel_5 = BodyLabel(self.ElevatedCardWidget)
        self.BodyLabel_5.setObjectName("BodyLabel_5")
        self.verticalLayout_6.addWidget(self.BodyLabel_5)
        self.verticalLayout_5.addWidget(self.ElevatedCardWidget)
        spacerItem2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem2)
        self.CaptionLabel = CaptionLabel(self)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.verticalLayout_5.addWidget(self.CaptionLabel)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.verticalLayout_5.addItem(spacerItem3)
        spacerItem4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.gridLayout_2.addLayout(self.verticalLayout_5, 3, 1, 1, 1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.StrongBodyLabel_2 = StrongBodyLabel(self)
        self.StrongBodyLabel_2.setObjectName("StrongBodyLabel_2")
        self.verticalLayout.addWidget(self.StrongBodyLabel_2)
        spacerItem5 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem5)
        self.ListWidget_2 = ListWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.ListWidget_2.sizePolicy().hasHeightForWidth())
        self.ListWidget_2.setSizePolicy(sizePolicy)
        self.ListWidget_2.setObjectName("ListWidget_2")
        self.verticalLayout.addWidget(self.ListWidget_2)
        spacerItem6 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem6)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.PrimaryPushButton_2 = PrimaryPushButton(self)
        self.PrimaryPushButton_2.setObjectName("PrimaryPushButton_2")
        self.horizontalLayout_2.addWidget(self.PrimaryPushButton_2)
        spacerItem7 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.PushButton = PushButton(self)
        self.PushButton.setObjectName("PushButton")
        self.horizontalLayout_2.addWidget(self.PushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout, 3, 0, 1, 1)
        spacerItem8 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem8, 1, 0, 1, 2)

        self.fetchOnlineThread = FetchOnline()
        self.fetchOnlineThread.callback.connect(self.fetchOnlineCallback)
        self.PrimaryPushButton_2.setEnabled(False)
        self.PushButton.setEnabled(False)
        self.ListWidget_2.clicked.connect(self.clickOnline)
        self.PushButton.clicked.connect(self.fetch)
        self.fetchOnlineContentThread = FetchOnlineContent()
        self.fetchOnlineContentThread.callback.connect(self.fetchAttentionCallback)
        self.PrimaryPushButton_2.clicked.connect(self.enterExam)
        self.BodyLabel.setText("")
        self.BodyLabel_2.setText("")
        self.BodyLabel_3.setText("")
        self.BodyLabel_4.setText("")
        self.BodyLabel_5.setText("")
        self.onlineList = []
        self.token = None
        self.page = 0

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "ZhiXueHacker"))
        self.CaptionLabel_3.setText(_translate("Form", ""))
        self.TitleLabel.setText(_translate("Form", "在线考试"))
        self.StrongBodyLabel.setText(_translate("Form", "Copyright © 2024-2025 HShiDianLu. All Rights Reserved."))
        self.CaptionLabel_2.setText(_translate("Form", "Version " + VERSION))
        self.StrongBodyLabel_3.setText(_translate("Form", "考试详情"))
        self.BodyLabel.setText(_translate("Form", ""))
        self.BodyLabel_3.setText(_translate("Form", ""))
        self.BodyLabel_4.setText(_translate("Form", ""))
        self.BodyLabel_2.setText(_translate("Form", ""))
        self.BodyLabel_5.setText(_translate("Form", ""))
        self.CaptionLabel.setText(_translate("Form", "注：目前在线考试仅能查看/复制题目，由于API原因不能提交。"))
        self.StrongBodyLabel_2.setText(_translate("Form", "在线考试列表"))
        self.PrimaryPushButton_2.setText(_translate("Form", "进入考试"))
        self.PushButton.setText(_translate("Form", "加载更多"))

    def login(self, username, token):
        self.CaptionLabel_3.setText(username + "同学")
        self.token = token
        self.fetchOnlineThread.setPat(self.token, self.page)
        self.fetchOnlineThread.start()

    def logout(self):
        self.PrimaryPushButton_2.setEnabled(False)
        self.PushButton.setEnabled(False)
        self.BodyLabel.setText("")
        self.BodyLabel_2.setText("")
        self.BodyLabel_3.setText("")
        self.BodyLabel_4.setText("")
        self.BodyLabel_5.setText("")
        self.CaptionLabel_3.setText("")
        self.onlineList = []
        self.token = None
        self.page = 0
        self.ListWidget_2.clearSelection()
        self.ListWidget_2.clear()
        self.PrimaryPushButton_2.setText("进入考试")
        self.PushButton.setText("加载更多")

    def fetch(self):
        self.PushButton.setEnabled(False)
        self.page += 1
        self.fetchOnlineThread.setPat(self.token, self.page)
        self.fetchOnlineThread.start()

    def clickOnline(self):
        self.PrimaryPushButton_2.setEnabled(True)
        self.PrimaryPushButton_2.setText("进入考试")
        cur = self.ListWidget_2.currentRow()
        print(cur)
        self.BodyLabel.setText("名称：" + self.onlineList[cur]['examName'])
        self.BodyLabel_3.setText("ID：" + self.onlineList[cur]['id'])
        self.BodyLabel_4.setText(
            "学科：" + self.onlineList[cur]['subjectName'] + " (" + self.onlineList[cur]['subjectCode'] + ")")
        start = self.onlineList[cur]['startTime']
        end = self.onlineList[cur]['endTime']
        delta = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(start,
                                                                                                  "%Y-%m-%d %H:%M:%S")
        self.BodyLabel_2.setText(
            "时间：" + start + " - " + end + " (" + str(round((delta.days * 86400 + delta.seconds) / 60)) + " 分钟)")
        delta2 = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()
        delta3 = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()
        if self.onlineList[cur]['status'] == 1:
            # self.PrimaryPushButton_2.setEnabled(False)
            self.PrimaryPushButton_2.setText("考试未开始")
            m, s = divmod(self.onlineList[cur]['remainTime'], 60)
            m1, s1 = divmod(self.onlineList[cur]['signRemainTime'], 60)
            additional = ""
            # additional = "（已可进入考场）"
            # if self.onlineList[cur]['signRemainTime'] != 0:
            #     if m1 > 15:
            #         additional = "（" + str(m1) + " 分钟后可进入考场）"
            #     else:
            #         additional = "（" + str(m1) + " 分 " + str(s1) + " 秒后可进入考场）"
            # if self.onlineList[cur]['signRemainTime'] > 1800:
            #     additional = ""
            if m > 30:
                self.BodyLabel_5.setText("距离开始：" + str(m) + " 分钟" + additional)
            else:
                self.BodyLabel_5.setText("距离开始：" + str(m) + " 分 " + str(s) + " 秒" + additional)
        elif self.onlineList[cur]['status'] == 2:
            m, s = divmod((delta2.days * 86400 + delta2.seconds), 60)
            if m > 30:
                self.BodyLabel_5.setText("距离结束：" + str(m) + " 分钟")
            else:
                self.BodyLabel_5.setText("距离结束：" + str(m) + " 分 " + str(s) + " 秒")
        elif self.onlineList[cur]['status'] == 0:
            self.PrimaryPushButton_2.setEnabled(False)
            self.PrimaryPushButton_2.setText("考试未开始")
            if delta3.days != 0:
                self.BodyLabel_5.setText(
                    "距离开始：" + str(delta2.days) + " 天 " + str(round(delta3.seconds / 3600)) + " 小时")
            else:
                if delta3.seconds / 3600 < 1:
                    m, s = divmod(delta3.seconds, 60)
                    if m > 30:
                        self.BodyLabel_5.setText("距离开始：" + str(m) + " 分钟")
                    else:
                        self.BodyLabel_5.setText("距离开始：" + str(m) + " 分 " + str(s) + " 秒")
                else:
                    self.BodyLabel_5.setText("距离开始：" + str(round(delta3.seconds / 3600)) + " 小时")

    def enterExam(self):
        self.PrimaryPushButton_2.setEnabled(False)
        self.fetchOnlineContentThread.setPat(self.token, self.onlineList[self.ListWidget_2.currentRow()]['id'])
        self.fetchOnlineContentThread.start()

    def fetchOnlineCallback(self, success, info, onlineTmpList, totalPage):
        if success:
            if self.page + 1 >= totalPage:
                self.PushButton.setText("没有更多了")
                self.PushButton.setEnabled(False)
            else:
                self.PushButton.setEnabled(True)
            for i in onlineTmpList:
                self.onlineList.append(i)
                self.ListWidget_2.addItem(QListWidgetItem(i['examName'] + " (" + i['id'] + ")"))
        else:
            InfoBar.error(
                title="在线考试列表获取失败",
                content="错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )
            self.PushButton.setEnabled(True)

    def fetchAttentionCallback(self, success, info):
        self.PrimaryPushButton_2.setEnabled(True)
        if success:
            w = MessageBox("考试要求", info, self)
            w.yesButton.setText("跳转至至考试页面")
            w.cancelButton.hide()
            cur = self.ListWidget_2.currentRow()
            start = self.onlineList[cur]['startTime']
            end = self.onlineList[cur]['endTime']
            delta = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(start,
                                                                                                      "%Y-%m-%d %H:%M:%S")
            self.examSignal.emit(self.onlineList[cur]['examName'],
                                 self.onlineList[cur]['subjectName'],
                                 self.onlineList[cur]['id'], delta.days * 86400 + delta.seconds)
            if w.exec():
                self.examSwitchSignal.emit()
        else:
            InfoBar.error(
                title="考试要求获取失败",
                content="错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )


class AnswerUi(WindowType):
    def __init__(self):
        super().__init__()
        self.setObjectName("Answer")
        self.resize(552, 230)
        if isDarkTheme():
            self.setStyleSheet(DARKQSS)
        else:
            self.setStyleSheet(LIGHTQSS)
        ico_path = os.path.join(os.path.dirname(__file__), FILEDIR + "/ZhiXueIcon.ico")
        icon = QIcon()
        icon.addPixmap(QPixmap(ico_path), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.gridLayout_2 = QGridLayout(self)
        self.gridLayout_2.setContentsMargins(20, 40, 20, 15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.TitleLabel = TitleLabel(self)
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout.addWidget(self.TitleLabel)
        self.CaptionLabel = CaptionLabel(self)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.verticalLayout.addWidget(self.CaptionLabel)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_2.addLayout(self.verticalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.PrimaryPushButton_2 = PrimaryPushButton(self)
        self.PrimaryPushButton_2.setObjectName("PrimaryPushButton_2")
        self.horizontalLayout_4.addWidget(self.PrimaryPushButton_2)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)
        spacerItem16 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem16, 1, 0, 1, 1)

        self.setWindowModality(Qt.ApplicationModal)
        self.PrimaryPushButton_2.clicked.connect(self.close)
        self.answerList = []

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", ""))
        self.TitleLabel.setText(_translate("Form", "答案查看"))
        self.CaptionLabel.setText(_translate("Form", ""))
        self.PrimaryPushButton_2.setText(_translate("Form", "关闭"))

    def setup(self, topicDetailList, title):
        self.setWindowTitle("答案查看 - 第 " + title + " 题")
        self.CaptionLabel.setText("第 " + title + " 题")
        self.answerList = topicDetailList
        self.resize(552, 190 + len(topicDetailList) * 40)
        self.setFixedSize(self.width(), self.height())
        for i in topicDetailList:
            print(i)
            self.horizontalLayout = QHBoxLayout()
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.BodyLabel = BodyLabel(self)
            self.BodyLabel.setObjectName("BodyLabel")
            self.horizontalLayout.addWidget(self.BodyLabel)
            spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.horizontalLayout.addItem(spacerItem1)
            if i['topicType'] == 1:
                # Radio
                self.BodyLabel.setText(i['answerDispTitle'] + ".（单选题）")
                self.buttonGroup = QButtonGroup(self)
                for j in range(len(i['objOpts'])):
                    self.RadioButton = RadioButton(self)
                    # self.RadioButton.setEnabled(False)
                    self.RadioButton.setText(i['objOpts'][j])
                    self.buttonGroup.addButton(self.RadioButton)
                    try:
                        for k in i['answer']:
                            if k == i['objOpts'][j]:
                                self.RadioButton.setChecked(True)
                    except:
                        pass
                    self.horizontalLayout.addWidget(self.RadioButton)
                    if i == len(i['objOpts']) - 1:
                        continue
                    spacerItem2 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
                    self.horizontalLayout.addItem(spacerItem2)
                spacerItem5 = QSpacerItem(15, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
                self.horizontalLayout.addItem(spacerItem5)
            elif i['topicType'] == 3:
                # Checkbox
                self.BodyLabel.setText(i['answerDispTitle'] + ".（多选题）")
                for j in range(len(i['objOpts'])):
                    self.CheckBox = CheckBox(self)
                    # self.CheckBox.setEnabled(False)
                    self.CheckBox.setText(i['objOpts'][j])
                    try:
                        for k in i['answer']:
                            if k == i['objOpts'][j]:
                                self.CheckBox.setChecked(True)
                    except:
                        pass
                    self.horizontalLayout.addWidget(self.CheckBox)
                    if i == len(i['objOpts']) - 1:
                        continue
                    spacerItem8 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
                    self.horizontalLayout.addItem(spacerItem8)
            else:
                # Submit
                print("Submit", i['topicType'])
                self.BodyLabel.setText(i['answerDispTitle'] + ".（答案提交型题 [" + str(i['topicType']) + "]）")
                spacerItem12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
                self.horizontalLayout.addItem(spacerItem12)
                # self.PrimaryPushButton = PrimaryPushButton(self)
                # self.PrimaryPushButton.setText("上传文件")
                # self.horizontalLayout.addWidget(self.PrimaryPushButton)
                # spacerItem13 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
                # self.horizontalLayout.addItem(spacerItem13)
                # self.PushButton = PushButton(self)
                # self.PushButton.setText("查看当前文件")
                # self.horizontalLayout.addWidget(self.PushButton)
                # spacerItem14 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
                # self.horizontalLayout.addItem(spacerItem14)
                self.BodyLabel_4 = BodyLabel(self)
                if i['answer']:
                    self.BodyLabel_4.setText("已上传 " + str(len(i['answer'])) + " / " + str(i['subLimit']))
                else:
                    self.BodyLabel_4.setText("未上传 0 / " + str(i['subLimit']))
                self.horizontalLayout.addWidget(self.BodyLabel_4)
                # spacerItem15 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
                # self.horizontalLayout.addItem(spacerItem15)
                # self.ToolButton = ToolButton(self)
                # self.ToolButton.setIcon(FIF.DELETE)
                # self.horizontalLayout.addWidget(self.ToolButton)
            self.verticalLayout_2.addLayout(self.horizontalLayout)
            spacerItem6 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
            self.verticalLayout_2.addItem(spacerItem6)


class ExamUi(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Exam")
        # self.resize(750, 599)
        font = QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(10)
        self.setFont(font)
        # self.setStyleSheet("")
        self.gridLayout_2 = QGridLayout(self)
        self.gridLayout_2.setContentsMargins(20, 15 + windowOffset, 20, 15)
        self.gridLayout_2.setHorizontalSpacing(24)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.CaptionLabel_4 = CaptionLabel(self)
        self.CaptionLabel_4.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.CaptionLabel_4.setObjectName("CaptionLabel_4")
        self.gridLayout.addWidget(self.CaptionLabel_4, 1, 1, 1, 1)
        self.CaptionLabel_3 = CaptionLabel(self)
        self.CaptionLabel_3.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.CaptionLabel_3.setObjectName("CaptionLabel_3")
        self.gridLayout.addWidget(self.CaptionLabel_3, 0, 1, 1, 1)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.TitleLabel = TitleLabel(self)
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout_4.addWidget(self.TitleLabel)
        self.CaptionLabel = CaptionLabel(self)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.verticalLayout_4.addWidget(self.CaptionLabel)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 2, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 4, 0, 1, 3)
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 7, 0, 1, 2)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.StrongBodyLabel_3 = StrongBodyLabel(self)
        self.StrongBodyLabel_3.setObjectName("StrongBodyLabel_3")
        self.verticalLayout.addWidget(self.StrongBodyLabel_3)
        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setSpacing(5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout.addLayout(self.gridLayout_4)
        spacerItem2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.PrimaryPushButton_2 = PrimaryPushButton(self)
        self.PrimaryPushButton_2.setObjectName("PrimaryPushButton_2")
        self.verticalLayout.addWidget(self.PrimaryPushButton_2)
        spacerItem3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.gridLayout_2.addLayout(self.verticalLayout, 10, 2, 4, 1)
        self.ProgressBar = ProgressBar(self)
        self.ProgressBar.setProperty("value", 45)
        self.ProgressBar.setInvertedAppearance(False)
        self.ProgressBar.setUseAni(True)
        self.ProgressBar.setObjectName("ProgressBar")
        self.gridLayout_2.addWidget(self.ProgressBar, 6, 0, 1, 3)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.StrongBodyLabel_2 = StrongBodyLabel(self)
        self.StrongBodyLabel_2.setObjectName("StrongBodyLabel_2")
        self.horizontalLayout.addWidget(self.StrongBodyLabel_2)
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.PrimaryToolButton_2 = PrimaryToolButton(self)
        self.PrimaryToolButton_2.setObjectName("PrimaryToolButton_2")
        self.horizontalLayout.addWidget(self.PrimaryToolButton_2)
        spacerItem5 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.PrimaryToolButton = PrimaryToolButton(self)
        self.PrimaryToolButton.setText("")
        self.PrimaryToolButton.setObjectName("PrimaryToolButton")
        self.horizontalLayout.addWidget(self.PrimaryToolButton)
        spacerItem6 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.ToolButton = ToolButton(self)
        self.ToolButton.setObjectName("ToolButton")
        self.horizontalLayout.addWidget(self.ToolButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        spacerItem7 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem7)
        self.TextEdit = TextEdit(self)
        self.TextEdit.setReadOnly(True)
        self.TextEdit.setObjectName("TextEdit")
        self.verticalLayout_5.addWidget(self.TextEdit)
        spacerItem8 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem8)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.PrimaryPushButton = PrimaryPushButton(self)
        self.PrimaryPushButton.setObjectName("PrimaryPushButton")
        self.horizontalLayout_2.addWidget(self.PrimaryPushButton)
        spacerItem9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem9)
        self.PrimaryPushButton_3 = PrimaryPushButton(self)
        self.PrimaryPushButton_3.setObjectName("PrimaryPushButton_3")
        self.horizontalLayout_2.addWidget(self.PrimaryPushButton_3)
        spacerItem10 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem10)
        self.CaptionLabel_5 = CaptionLabel(self)
        self.CaptionLabel_5.setObjectName("CaptionLabel_5")
        self.horizontalLayout_2.addWidget(self.CaptionLabel_5)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout_5, 10, 0, 1, 2)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.StrongBodyLabel = StrongBodyLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.StrongBodyLabel.setFont(font)
        self.StrongBodyLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.verticalLayout_3.addWidget(self.StrongBodyLabel)
        self.CaptionLabel_2 = CaptionLabel(self)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.CaptionLabel_2.setFont(font)
        self.CaptionLabel_2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.CaptionLabel_2.setObjectName("CaptionLabel_2")
        self.verticalLayout_3.addWidget(self.CaptionLabel_2)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 17, 0, 1, 3)
        spacerItem11 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem11, 15, 0, 1, 3)
        spacerItem12 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem12, 5, 0, 1, 3)

        self.ToolButton.setIcon(FIF.COPY)
        self.PrimaryToolButton_2.setIcon(FIF.LEFT_ARROW)
        self.PrimaryToolButton.setIcon(FIF.RIGHT_ARROW)
        self.token = None
        self.username = None
        self.PrimaryToolButton_2.setEnabled(False)
        self.PrimaryToolButton.setEnabled(False)
        self.ToolButton.setEnabled(False)
        self.PrimaryPushButton_2.setEnabled(False)
        self.TextEdit.setEnabled(False)
        self.ProgressBar.setValue(0)
        self.ProgressBar.setVisible(False)
        self.timer = TickTimer()
        self.timer.start()
        self.timer.tick.connect(self.timeUpdate)
        self.syncer = TimeSyncer()
        self.syncer.setPat(None, None)
        self.syncer.start()
        self.syncer.value.connect(self.countdownCallback)
        self.timeLeft = -1
        self.state = False
        self.examId = None
        self.btnGroup = []
        self.problemList = []
        self.PrimaryPushButton_3.setEnabled(False)
        self.fetchProblemThread = FetchProblem()
        self.fetchProblemThread.callback.connect(self.problemCallback)
        self.nowSelect = 0
        self.lastSelect = 0
        self.ToolButton.clicked.connect(self.copy)
        self.PrimaryToolButton.clicked.connect(lambda: self.turnPage(1))
        self.PrimaryToolButton_2.clicked.connect(lambda: self.turnPage(-1))
        self.PrimaryPushButton_3.clicked.connect(self.showAnswer)
        self.PrimaryPushButton_2.setVisible(False)
        self.PrimaryPushButton.setEnabled(False)
        self.PrimaryPushButton.clicked.connect(self.showProblemDetail)
        self.fullTime = 1

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "ZhiXueHacker"))
        self.StrongBodyLabel.setText(_translate("Form", "Copyright © 2024-2025 HShiDianLu. All Rights Reserved."))
        self.CaptionLabel_2.setText(_translate("Form", "Version " + VERSION))
        self.StrongBodyLabel_2.setText(_translate("Form", ""))
        self.CaptionLabel_4.setText(_translate("Form", ""))
        self.CaptionLabel_3.setText(_translate("Form", ""))
        self.TitleLabel.setText(_translate("Form", "在线考试"))
        self.CaptionLabel.setText(_translate("Form", "考试名称：无 | 学科：无"))
        self.StrongBodyLabel_3.setText(_translate("Form", "题目列表"))
        self.PrimaryPushButton_2.setText(_translate("Form", "交卷"))
        self.PrimaryPushButton_3.setText(_translate("Form", "查看提交答案"))
        self.CaptionLabel_5.setText(_translate("Form", ""))
        self.PrimaryPushButton.setText(_translate("Form", "题目详情（Latex / 图片显示）"))

    def login(self, username, token):
        self.username = username
        self.token = token

    def logout(self, keepVar=False):
        if not keepVar:
            self.token = None
            self.username = None
        self.PrimaryToolButton_2.setEnabled(False)
        self.PrimaryToolButton.setEnabled(False)
        self.ToolButton.setEnabled(False)
        self.PrimaryPushButton_2.setEnabled(False)
        self.TextEdit.setEnabled(False)
        self.ProgressBar.setValue(0)
        self.ProgressBar.setVisible(False)
        self.CaptionLabel.setText("考试名称：无 | 学科：无")
        self.CaptionLabel_4.setText("")
        self.CaptionLabel_3.setText("")
        self.CaptionLabel_5.setText("")
        self.PrimaryPushButton_3.setEnabled(False)
        self.syncer.setPat(None, None)
        self.state = False
        self.examId = None
        items = list(range(self.gridLayout_4.count()))
        items.reverse()
        for i in items:
            item = self.gridLayout_4.itemAt(i)
            self.gridLayout_4.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
        self.btnGroup = []
        self.problemList = []
        self.nowSelect = 0
        self.lastSelect = 0
        self.TextEdit.setText("")
        self.StrongBodyLabel_2.setText("")
        self.PrimaryPushButton.setEnabled(False)
        self.fullTime = 1

    def setTitle(self, examName, subjectName, examId, fullTime):
        self.logout(True)
        self.ProgressBar.setVisible(True)
        self.ProgressBar.setValue(0)
        self.CaptionLabel_3.setText(self.username + "同学")
        self.CaptionLabel.setText("考试名称：" + examName + " | 学科：" + subjectName)
        self.examId = examId
        self.syncer.setPat(self.token, self.examId)
        self.fetchProblemThread.setPat(self.token, self.examId, [1])
        self.TextEdit.setEnabled(True)
        self.PrimaryPushButton_2.setEnabled(True)
        self.ToolButton.setEnabled(True)
        self.fullTime = fullTime
        print(self.fullTime)

    def selectProblem(self, num):
        self.lastSelect = self.nowSelect
        self.nowSelect = num
        print(num, self.lastSelect)
        self.btnGroup[self.lastSelect].setChecked(False)
        for i in range(len(self.problemList)):
            self.btnGroup[i].setEnabled(False)
        self.fetchProblemThread.setPat(self.token, self.examId, self.problemList[num]['topicNums'])
        self.fetchProblemThread.start()
        self.PrimaryToolButton.setEnabled(False)
        self.PrimaryToolButton_2.setEnabled(False)

    def turnPage(self, direction):
        self.selectProblem(self.nowSelect + direction)

    def countdownCallback(self, success, info, timeLeft):
        if success:
            m, s = divmod(timeLeft, 60)
            self.CaptionLabel_4.setText("距离结束：" + str(m) + " 分 " + str(s) + " 秒")
            self.state = True
            self.timeLeft = timeLeft
        else:
            InfoBar.error(
                title="剩余时间获取失败",
                content="错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )

    def timeUpdate(self):
        self.timeLeft -= 1
        self.ProgressBar.setValue(min(max(round((self.fullTime - self.timeLeft) / self.fullTime * 100), 0), 100))
        m, s = divmod(self.timeLeft, 60)
        if self.state:
            self.CaptionLabel_4.setText("距离结束：" + str(m) + " 分 " + str(s) + " 秒")

    def funcConstruct(self, i):
        return lambda: self.selectProblem(i)

    def problemListCallback(self, success, info, problem):
        if success:
            self.problemList = problem
            for i in range(len(problem)):
                self.btnGroup.append(PillPushButton(self))
                self.btnGroup[i].setText(problem[i]['dispTitle'])
                self.btnGroup[i].clicked.connect(self.funcConstruct(i))
                x, y = divmod(i, 5)
                self.gridLayout_4.addWidget(self.btnGroup[i], x, y, 1, 1)
            self.btnGroup[0].setChecked(True)
            self.fetchProblemThread.start()
            self.StrongBodyLabel_2.setText("第 " + self.problemList[0]['dispTitle'] + " 题")
        else:
            InfoBar.error(
                title="题目列表获取失败",
                content="错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )

    def problemCallback(self, success, info):
        self.PrimaryPushButton.setEnabled(True)
        self.PrimaryPushButton_3.setEnabled(True)
        self.PrimaryToolButton.setEnabled(True)
        self.PrimaryToolButton_2.setEnabled(True)
        for i in range(len(self.problemList)):
            self.btnGroup[i].setEnabled(True)
        if success:
            self.StrongBodyLabel_2.setText("第 " + self.problemList[self.nowSelect]['dispTitle'] + " 题")
            print(info)
            self.TextEdit.setHtml(info)
            topics = self.problemList[self.nowSelect]['topicDetailList']
            count = 0
            for i in topics:
                print(i)
                if i['answer']:
                    count += 1
            if len(topics) == 1 and count == 1:
                self.CaptionLabel_5.setText("已提交")
            elif len(topics) == 1 and count == 0:
                self.CaptionLabel_5.setText("未提交")
            else:
                self.CaptionLabel_5.setText("已提交 " + str(count) + " / " + str(len(topics)))
        else:
            self.btnGroup[self.nowSelect].setChecked(False)
            self.btnGroup[self.lastSelect].setChecked(True)
            self.nowSelect = self.lastSelect
            InfoBar.error(
                title="题目获取失败",
                content="错误信息：" + displayError(info),
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=5000,
                parent=self
            )
        self.btnGroup[self.nowSelect].setChecked(True)
        if self.nowSelect == len(self.problemList) - 1:
            self.PrimaryToolButton.setEnabled(False)
        if self.nowSelect == 0:
            self.PrimaryToolButton_2.setEnabled(False)

    def copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.TextEdit.toPlainText())
        InfoBar.success(
            title="复制成功",
            content="已将题目内容复制至剪贴板。",
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.BOTTOM,
            duration=3000,
            parent=self
        )

    def showAnswer(self):
        self.answer = AnswerUi()
        self.answer.setup(self.problemList[self.nowSelect]['topicDetailList'],
                          self.problemList[self.nowSelect]['dispTitle'])
        self.answer.show()

    def showProblemDetail(self):
        self.webView = WebViewUi()
        if isDarkTheme():
            css = "body{background-color: rgb(39, 39, 39)} #content *{color:white}"
        else:
            css = "body{background-color: rgb(240, 240, 240)}"
        problemHTML = '''
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <script src="https://cdn.jsdelivr.net/npm/mathjax@3.0.0/es5/tex-mml-chtml.js"></script>
                        <style>''' + css + '''</style>
                    </head>
                    <body>
                        <div id="content">
                        ''' + self.TextEdit.toHtml() + '''
                        </div>
                        <script type="text/javascript">
                            MathJax = {
                                tex: {inlineMath: [['$', '$'], ['\\(', '\\)']]}
                            };
                        </script>
                    </body>
                    </html>'''
        print(problemHTML)
        with open(FILEDIR + "/problemTemp.html", "w", encoding="utf-8") as f:
            f.write(problemHTML)
        self.webView.setup("file:///" + FILEDIR + "/problemTemp.html")
        self.webView.show()


class CustomTitleBar(TitleBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.window().windowIconChanged.connect(self.setIcon)

        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))


class StackedWidget(QFrame):
    currentChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(self.currentChanged)

    def addWidget(self, widget):
        self.view.addWidget(widget)

    def widget(self, index: int):
        return self.view.widget(index)

    def setCurrentWidget(self, widget, anim=True):
        if anim:
            self.view.setCurrentWidget(widget, False, False, 300, QEasingCurve.OutQuad)
        else:
            self.view.setCurrentWidget(widget, False, False, 0)

    def setCurrentIndex(self, index, anim=False):
        self.setCurrentWidget(self.view.widget(index), anim)


class MenuUiFrameless(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(
            self, showMenuButton=True, showReturnButton=True)
        self.stackWidget = StackedWidget(self)

        # self.windowEffect.setAcrylicEffect(self.winId(), "00000099")

        self.mainInterface = MainUi()
        self.aboutInterface = InfoUi()
        self.detailInterface = DetailUi()
        self.settingInterface = SettingUi()
        self.downloadInterface = DownloadUI()
        self.scoreDetailInterface = ScoreDetailUI()
        self.examListInterface = ExamListUi()
        self.examInterface = ExamUi()

        self.mainInterface.mainSignal.connect(self.detailInterface.activePage)
        self.mainInterface.mainSignal.connect(self.downloadInterface.activePage)
        self.mainInterface.mainSignal.connect(self.scoreDetailInterface.activePage)
        self.mainInterface.mainSignal.connect(lambda: self.switchTo(self.detailInterface))
        self.mainInterface.fetchRankThread.sheetCallback.connect(self.detailInterface.sheetCallback)
        self.mainInterface.fetchRankThread.problemCallback.connect(self.downloadInterface.problemCallback)
        self.mainInterface.fetchRankThread.scoreDetailCallback.connect(self.scoreDetailInterface.scoreDetailCallback)
        self.mainInterface.logoutSignal.connect(self.detailInterface.logout)
        self.mainInterface.logoutSignal.connect(self.downloadInterface.logout)
        self.mainInterface.logoutSignal.connect(self.scoreDetailInterface.logout)
        self.mainInterface.logoutSignal.connect(self.examListInterface.logout)
        self.mainInterface.logoutSignal.connect(self.examInterface.logout)
        self.mainInterface.loginSignal.connect(self.examListInterface.login)
        self.mainInterface.loginSignal.connect(self.examInterface.login)
        self.examListInterface.examSwitchSignal.connect(lambda: self.switchTo(self.examInterface))
        self.examListInterface.examSignal.connect(self.examInterface.setTitle)
        self.examListInterface.fetchOnlineContentThread.countdownCallback.connect(self.examInterface.countdownCallback)
        self.examListInterface.fetchOnlineContentThread.problemListCallback.connect(
            self.examInterface.problemListCallback)

        self.initLayout()

        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

        self.titleBar.raise_()
        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)

    def initNavigation(self):
        self.navigationInterface.setAcrylicEnabled(True)

        self.addSubInterface(self.mainInterface, FIF.HOME, '首页')
        self.addSubInterface(self.detailInterface, FIF.PIE_SINGLE, '学科概览')
        self.addSubInterface(self.scoreDetailInterface, FIF.IOT, '得分详情')
        self.addSubInterface(self.downloadInterface, FIF.DOWNLOAD, '试卷生成')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.examListInterface, FIF.ALIGNMENT, '在线考试列表')
        self.addSubInterface(self.examInterface, FIF.PENCIL_INK, '在线考试')
        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.aboutInterface, FIF.INFO, '关于', NavigationItemPosition.BOTTOM)

        qrouter.setDefaultRouteKey(self.stackWidget, self.aboutInterface.objectName())

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.switchTo(self.aboutInterface, False)
        self.stackWidget.setCurrentIndex(0, False)

    def initWindow(self):
        self.resize(870, 620)
        ico_path = os.path.join(os.path.dirname(__file__), FILEDIR + "/ZhiXueIcon.ico")
        icon = QIcon()
        icon.addPixmap(QPixmap(ico_path), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle('ZhiXueHacker | ' + VERSION)
        self.setMinimumSize(self.width(), self.height())

        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.setQss()

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP):
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text
        )

    def setQss(self):
        if isDarkTheme():
            self.setStyleSheet(DARKQSS)
        else:
            self.setStyleSheet(LIGHTQSS)

    def switchTo(self, widget, anim=True):
        self.stackWidget.setCurrentWidget(widget, anim)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())
        qrouter.push(self.stackWidget, widget.objectName())

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width() - 46, self.titleBar.height())


class MenuUiFluent(FluentWindow):

    def __init__(self):
        super().__init__()

        self.hBoxLayout = QHBoxLayout(self)

        self.mainInterface = MainUi()
        self.aboutInterface = InfoUi()
        self.detailInterface = DetailUi()
        self.settingInterface = SettingUi()
        self.downloadInterface = DownloadUI()
        self.scoreDetailInterface = ScoreDetailUI()
        self.examListInterface = ExamListUi()
        self.examInterface = ExamUi()

        self.mainInterface.mainSignal.connect(self.detailInterface.activePage)
        self.mainInterface.mainSignal.connect(self.downloadInterface.activePage)
        self.mainInterface.mainSignal.connect(self.scoreDetailInterface.activePage)
        self.mainInterface.mainSignal.connect(lambda: self.switchTo(self.detailInterface))
        self.mainInterface.fetchRankThread.sheetCallback.connect(self.detailInterface.sheetCallback)
        self.mainInterface.fetchRankThread.problemCallback.connect(self.downloadInterface.problemCallback)
        self.mainInterface.fetchRankThread.scoreDetailCallback.connect(self.scoreDetailInterface.scoreDetailCallback)
        self.mainInterface.logoutSignal.connect(self.detailInterface.logout)
        self.mainInterface.logoutSignal.connect(self.downloadInterface.logout)
        self.mainInterface.logoutSignal.connect(self.scoreDetailInterface.logout)
        self.mainInterface.logoutSignal.connect(self.examListInterface.logout)
        self.mainInterface.logoutSignal.connect(self.examInterface.logout)
        self.mainInterface.loginSignal.connect(self.examListInterface.login)
        self.mainInterface.loginSignal.connect(self.examInterface.login)
        self.examListInterface.examSwitchSignal.connect(lambda: self.switchTo(self.examInterface))
        self.examListInterface.examSignal.connect(self.examInterface.setTitle)
        self.examListInterface.fetchOnlineContentThread.countdownCallback.connect(self.examInterface.countdownCallback)
        self.examListInterface.fetchOnlineContentThread.problemListCallback.connect(
            self.examInterface.problemListCallback)
        self.settingInterface.syncChange.connect(self.mainInterface.changeSyncState)

        self.initNavigation()

        self.initWindow()

    def initNavigation(self):
        self.navigationInterface.setAcrylicEnabled(True)

        self.addSubInterface(self.mainInterface, FIF.HOME, '首页')
        self.addSubInterface(self.detailInterface, FIF.PIE_SINGLE, '学科概览')
        self.addSubInterface(self.scoreDetailInterface, FIF.IOT, '得分详情')
        self.addSubInterface(self.downloadInterface, FIF.DOWNLOAD, '试卷生成')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.examListInterface, FIF.ALIGNMENT, '在线考试列表')
        self.addSubInterface(self.examInterface, FIF.PENCIL_INK, '在线考试')
        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.aboutInterface, FIF.INFO, '关于', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(870, 620)
        ico_path = os.path.join(os.path.dirname(__file__), FILEDIR + "/ZhiXueIcon.ico")
        icon = QIcon()
        icon.addPixmap(QPixmap(ico_path), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle('ZhiXueHacker | ' + VERSION)
        self.setMinimumSize(self.width(), self.height())

        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.setQss()

    def setQss(self):
        if isDarkTheme():
            self.setStyleSheet(DARKQSS)
        else:
            self.setStyleSheet(LIGHTQSS)

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width() - 46, self.titleBar.height())


def show_MainWindow():
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    if cfg.get(cfg.renderMethod) == "DesktopOpenGL":
        print("AA_UseDesktopOpenGL")
        QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)
    elif cfg.get(cfg.renderMethod) == "OpenGLES":
        print("AA_UseOpenGLES")
        QApplication.setAttribute(Qt.AA_UseOpenGLES)
    elif cfg.get(cfg.renderMethod) == "SoftwareOpenGL":
        print("AA_UseSoftwareOpenGL")
        QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
    if cfg.get(cfg.theme) == "Dark":
        setTheme(Theme.DARK)
    elif cfg.get(cfg.theme) == "Auto":
        setTheme(Theme.AUTO)
    else:
        setTheme(Theme.LIGHT)
    app = QApplication(sys.argv)
    if cfg.get(cfg.mica):
        ui = MenuUiFluent()
    else:
        ui = MenuUiFrameless()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    show_MainWindow()
