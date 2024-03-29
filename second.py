import redis
import random
import string

keysList = ['UO90rzqndD', 'ECo902rDbf', 'qGBLYcWQFL', 'zBBJcKDY62', '78OVXf7Sk6', 'yBrwqMofnk', 'zX9StzH7MA', 'C1zHDK79ha', 'zHUBKLvI0F', 'L6H0fwc2pQ', 'mUcgbyXvfD', 'mtrNhdNMF7', 'S3347ULooF', 'zha8v85Goj', 'sdGKwhHJ3m', 'NuABhzeset', '8l1gEHwzhZ', 'XSCer9Sx7K', 'JY1IY5TJw5', 'QBUZ1ZUpGP', '9jWgmUwfkq', 'swPsLWmmM8', 'BNt2UwIxAD', 'Psz6U7LfM8', 'b6hKDKdOAZ', 'ud2AsNlBW7', 'baaL9ZrDR8', 'jfvVdaERz5', 'irxEbWTjGH', 'fK21HpTLPW', 'szVauDK5ZY', 'OOCF11rp6I', 'MVxEZpydHt', 'vZS7o9J6lP', '4KreSBo5fI', 'pJ78Vs5EvT', 'ntfyXkqyzD', 'i5dr1UwRJo', 'sfNlqtedp5', 'GpAVpfW1s9', '9QidVRqg8M', 'jZNYRmbYmQ', 'AR3Jj29MHN', 'kCZ5480ruh', 'P7Xhv10eew', 'YLRmGiouTI', '20jz5Q5yUM', '4FqdIzpuYh', 'jAok6y6eZa', 'sHfI4zxHPc', 'acAX6e85Ld', 'TSC30WpXBZ', 'Wles8N53gw', 'hHUK3eE8AV', 'CKI8u8NOq5', 'udUGHDpljT', 'MLArU6zA5G', 'nKFdfhlMTF', 'QTRfPSADkC', 'lEhum4D0Kz', '5Tl3MJ8Okh', '1WHLUivoQJ', 'FH5lj7KHho', 'GLJBbTUQ8Y', 'EbBXdkKlLZ', 'f5L0xkmY2O', 'hWwHAkOrAc', '3ctbsU9RI6', 'fkKnpEQkWT', 'RKzRAPiEih', 'RsIzOsrn2m', '3vYuwyzyx3', 'TLMKGJ9cjm', 'u1WnrDsQbR', 'ZPUz1djWlJ', 'LraJk6Rkqf', 'uRDOvkomWK', 'y42NgHcrsV', 'aWTcNE3oV3', 'bHFRVaqWuM', '3dAdnztCk5', '4dShtjwEY7', 'Kir4NvWrIl', 'u35EIrflP6', 'R3Mj5VqTkn', 'POtZpqy85u', '0k02jhiErW', 'IKXcnSnIkQ', 'YdudHatUI7', 'J5zud9Pe5M', 'MRpolMuaq5', 'q3ysyOd18S', 'w7KgG3rXMV', 'U27ziPFCCB', 'tflYLnprwS', 'PgK25IoEsB', 'S0IqLL6pPd', 'IeN2Lx7mCa', '04Lr8sEH04', 'THEQxpXQVU', 'd96NdJdrgi', 'RdEikSXEpD', 'KjauTDbWxY', 'VXOI76JTeG', 'p7z5fZXYMN', 'RAsl0E0M2C', '4iuEgA3lnU', 'mr10RTCoTZ', '7v7EAIAoTB', '8iC7BktK6d', 'K86q03Juk1', 'TAMP7cEVE1', 'XYQyU4SUVH', 'nPetAgtrlR', 'qYgjOCwQCf', 'LLncWe3fjB', 'NwUMRSufbY', 'Bx9QkvvfmT', 'KqKBuZjNqW', 'OCpJTuWcZk', 'XctJ0r66DK', 'wpuQHSHcY0', 'iy9Iw9QtCC', '77XFr5pOUn', 'blrSTs3DJ2', 'nmLMj3oD6v', 'wveNIVafmb', 'mVRgPIB5pg', 'ymqOR85FVq', 'PDUDqtzhtH', 'eVbwWWdhOn', '5S8eR9U0gx', 'Uckhw2Azld', '5sHcz5NXbq', 'pcC6M2GoNc', 'pzPQxl3Qnh', '0Bf3nGWBZd', '03YMhJV1kT', '4eI9ngTpT9', 'HlfRvROHm0', 'gNAkk6AezK', '6uTjRsimGS', '8kjqM3hbpm', 'vKtcaz0v5i', 'Ie8cccdzvK', 'bHuPHPcHge', 'HoabnMXDGH', 'TX1uekE26H', 'FiHIYufqnb', '19ezdlkDR4', 'qaiQ3wjIAJ', 'KCs0tX30cg', 'MtieVx3RCq', 'UcNyFYc2xq', 'gJnpHRxOPM', 'getbtVORqd', 'Sw4r3Wu11y', 'BSaX9VuCJZ', 'MFPW7i7xwK', '7nexilK8HP', 'CJcnOMCdSL', 'mlollH06kl', 'IE6PyxQazW', 'oeJrDCYukE', 'GXFvM4AZv3', 'KfKpPsK1UH', 'mEKjDk7QRU', 'O9lcy5nD4x', 'UttqcFkZ4i', 'OKCvQoP9ZT', 'SS06jAbuwO', 'k1jZFtbqdY', 'LiIWdpQOez', 'l57tJneMtD', 'ulfHxl6ckh', 'sN0VMCBaWR', 'lZO9EGAXNp', 'tfr8NRTVbD', '7dRwDumWoA', '5rx2rPoyUp', 'kr7iCEZ9p1', 'lwNS19cSpR', '6DqIpmXkyd', 'GMBjZ6fZ8c', 'j5Phag8szr', 'MYrk2QEJBH', 'H5P4dP6yfm', 'xOIjmNYxOK', 'Z14mUc68Nq', 'CvplF74LKL', 'BZyfNVD5FD', 'FQ6gmXzEW0', 'lZ6RnjCNrn', 'No5bO6yX79', 'LIwDGvG9fe', 'sy2u5QMOr4', 'IYI8WeDclj', '2FCc0H6oqQ', 'LBZItO2tgY', 'nmuJSeycmb', 'E8fT5O586I', '8vKajA0hD2', 'OYn0O315TL', 'ntBZ7iJLv4', 'iFKyDAcdNU', 'sKWrad3nBA', 'DTIVP2hMP8', 'mtTm1VZukc', 'zRoongHgah', 'Tv3aaDQykA', 'l5XjnujYoB', 'mEliIX7sON', 'vIZpFc60FI', 'g1gMiDBA1J', 'zEk0N7Uvtm', 'ai8DpUXw35', 'bncP6Bi2Lh', 'o2jo9wj1Gd', 'o2RqgttZLS', 'Vpd3ykEHFp', '3R5PHXQDcq', 'Njue2plzXf', 'tGeMg1OcD8', 'ulwGIB2ROf', '9ScIFB2zeT', 'QQesGVmO0N', 'ehhv9LPWmX', 'qG3rhsCrUQ', 'AwE5vIqa8b', 'd8zxRaUCuU', 'nNF3oDKXUF', 'l38KzUdLRL', '55OSWSwvxV', 'J0Z1m0zR1r', 'jMCPw8akAh', 'vnTp1AM3Ea', 'y02ycw8MKY', '6jeQeZd8fH', 'XHQNSAJR9N', 'G0jV2bQVMJ', 'ICsBgqZhKi', 'CPn23VSFxI', 'nwMIpIn9TJ', 'ApRbfhGUGk', 'ey5JX5CLK3', 'KtoVmiD6QE', 'hQmY1Fyh6C', 'QckWJIL6hV', 'nKFXvjGSnr', 'WYncDUJYYk', 'WVSi6lMJmG', 'lNBimbb88I', 'Xgj6mGRZnW', '50zjIsZnQf', 'S93xFUHd8F', 'WzvUt8gZMg', '51eVuNj3TT', 'hCyFycsvBN', 'K1lUP2AKPi', 'nFxNbUQCEY', 'fU6LXmzCnj', 'sTmwNQZsKQ', 'UddB1s0vVe', 'n9AJVyKmWl', 'rWdgd2j7vP', '4ZVGycC8uk', '6BInWgFJVE', 'h0BLfqfGaN', 'EQdgyhbAgv', 'Xpn6vvI8xt', 'Cwbm2G1nK6', '4BPRUuwofL', 'OCFLS57jVr', '5HPMzOq5R1', 'ewTd9sel0L', 'oQrlRnuxoT', 'VvZ1paWlGy', 'XAKGe5P78y', 'oo7HSsyBVR', 'SFrL6fvSKy', 'Snp4W5ZYHu', 'rvSIteekOQ', 'evVecgkXu7', 'FFj70U9LwQ', 'Xbrwk8T0pH', 'yYOPkoA7mD', 'Vudkv70G3b', 'Opw5uv8aQC', 'i2jIz8QdCd', 'dANSoOX7wc', 'MJOMVOLIXl', 'mtCPWtDhfa', 'ObEdEVbQ35', 's4B83Hq55w', 'qw4WvLdBPp', 'lNuxdsmqDl', 'i0Yx0SyZte', 'JEyWHiXUQY', 'lmRMQmvUXF', 'CtJnltD4ge', 'MIG7rarnIi', 'VdJ6BsH55P', 'mB7ABMolGT', '1QcB4N9jk9', 'NS10DAbgdp', 'BbRVEbMAPq', 'E2sNbZ2uG0', 'YRMpXXTbfn', 'NSSPoKjPOm', 'RaRUgeSWqD', 'OGLNibOgYn', 'dNxHJxMlSk', 'MVW7FFeHta', 'CbBeqrcTG9', '8IuEh4vvvO', 'JqjHSJp07x', 'DS10HpolUN', 'ILW2MaDfWG', 'nf0VQC3GaH', '3neOXreqBy', 'OSEMdueh9e', '3UvUHBcFth', 'B2rY0NhDt1', 'bOQDbWL9PM', 's9k6cqBJHI', '2YeybIHPPP', 'tChGMMRhK7', 't9kzqwFxFS', '2g4bGlHGhK', 'mecJhlCoHj', 'KKxhch7bGg', 'p06vmbwfLs', 'ksM713n1aJ', 'O1TZcWsKvc', 'ggNaZCBvcl', '9v245RNXmi', '37BCGYV53l', 'ZtKgusMWFQ', 'YaMmIqxEr6', 'UikI9Z9d3a', 'jDVdevuBBj', 'MgJsXHcCKF', 'Gi0NUjBXXC', 'lJoEpxIH1Y', 'EN6X7lAAFh', '1n2aXkybhx', 'kWGAKhZ5d1', 'OpBgW9nS11', 'DjCo2RdmiL', 'VcUvIKQRah', 'x3YSR153Ef', 'sYL34RFqkZ', 'EhSeMgeZ0O', 'e6gUI3mo7p', 'tYebLKtFpt', 'tJ283bg4FL', 'NDuNkTOLBv', 'MIe8Dbbvg1', 'rPurRFhrlV', 'HF0ispNjl8', 'VbkzGS5Eej', 'i3mFjyTzFB', 'dCtVNFzplc', '3wkgQZXnSS', 'FKh6W8rb3f', 'lWkYfx2agl', 'wbGrYCfSxu', 'ZEgfKqzopP', 'kTrxa6fWOI', 'cocppOxhd5', 'F9SRlUmeJq', 'ccXxDz0MD6', 'RFxYjJmWQ2', 'fFtxoZUhp9', 'RzZdf47KZ5', 'eLDzitk2Xs', 'ID4C0BzwIt', '6cev1qp2zn', 'xi2rTt37Wa', 'zttNy52nuy', 'uAUEoEL6hP', 'tslzamfUr7', 'SETvrel7qP', '3rb5fVjRQs', 'CQhoIOB6aq', 'PkuddGljTP', 'LB5Xtc83jK', 'rGGbID1Vzu', 'uYqVkLaHqP', 'jiik00Vq9b', 'qSqipE3hBD', '6sF6iay5Xw', 'vmxUOj2H7G', 'I7Dzs2BACu', 'tRcBapm12f', 'YP6ODTzBVK', 'hOZDqLBHhr', 'hpD9IMSXG9', 'DQsLJE1pOV', 'oxeDoQo5oD', 'M6CYmFqQTb', 'kbgSlKaRgG', 'h8QQ5ESytx', '351MnLh4tp', 'ENNelrva50', '2BUajZBfDP', 'HKrlk9akIB', 'HIsVVR5GGO', 'YoEvnlg8DP', 'Nvd7ZRmtsq', '2uQOCUsdmH', 'pT7yeCU7KF', 'lC9uwvcq3s', '540MB6jPG9', '8AlipAb3GJ', 'FFwGX4MMO0', 'NllzPf3MFk', '9zMkYkqoPE', 'TEzcVdjErR', 'RAokx6L0QI', 'v86YUmguhX', 'jUJgDpRVuL', 'yXWONsG9VC', '1fIQ3gZGLh', 'K0onuEI2kO', 'iYA2Z5Dmye', 'CuNmwoXzwN', 'MQcZZVcERG', 'thAI97H1Dw', 'VU4XbKbyoA', 'OaahlnM4mR', 'GXBBanWPcE', 'JV2sbAK3yo', 'Cvw5VeDyrV', 'fvFAXJNHgP', 'Ap1csMpKgh', 'Z2xfQSpagj', 'uKAYz0Z3PM', '6n2mDOiuUO', 'e2pIZ7abPS', 'Utxr5qcTEY', 'r7h6GXITYd', 'v8A1AKu60a', 'yvCY7vTwCj', 'Fkg6ZsAI62', 'F5KQ99RvaH', 'Wc6niEJeYg', 'eU1ZUQiwbE', 'SDiHjavf8s', 'U8bQ34fxsW', 'fmiNKCnSnf', '96Gl7cfgy8', 'QrqHM0CA8s', 'D6AGXLp5y7', 'mHJJZi3RaJ', '9QGyYXpPPs', '4o2zfpLbzd', 'Olgy3GTiV1', 's43oZAOmop', 'YZfKI58ek9', 'Sh5arkcSSh', 'cWGlY0onUd', 'kKyqnrlHP8', 'SLIrjztp1D', '5WqxP1yUkn', 'ow7ufSTSEi', '4LsUAvi3Md', 'Xiytk3WZ7H', '6fUzZwiY7n', 'LRZhA0cS0a', 'oMZgKv2zpj', 'hUI3tlgxfl', 'TuiTU2CYka', 'gxyzrHwIC5', 'aSfTJlVN5Y', 'dc14R4U9S0', 'QOQW6fAfBI', 'fmgNfGG155', 'fqa2SU5Gmt', 'gJFAZ8sqhx', 'b5yXJFVSeF', 'uCqnep0VCV', 'mkjl2k4V89', '1apr4EHIJ4', 'OaGPiJ01Yj', 'CkVzNOKWXA', 'ZJfrhjKlbb', 'reZZPW7CXz', '1AvtWrAK5E', '2oslThuCd6', 'oIvzTXNvEw', 'uK2ZzHUYaW', 'aow2fqCBD2', 'AxRriR6Gsw', 'yPJXDUP2u2', 'zWcl3sp8rA', 'caBrd3qkdY', 'eJg0WSZWXo', 'qcaWt6PBc1', 'hf69YXSpaP', '1vApb9oQnP', 'CbAZK7eFJY', 'RubmoYpo0D', 'uhPbV012pI', 'i6g5sDzOhb', 'pzAcZEI9xa', 'dI14iXVV8B', 'FfuYocPXdQ', '7bMlQt8lgz', 'XH0gXeHZxu', 'F2Ra06mrM1', '9Y8TiUzjMO', 'lGVb2c9sBg', 'dFscUae5Kl', 'rRciyUbZFD', 'c8wR1KMZSH', 'r5Q5M7RcvQ', 'DGqFTd3nwg', 'QdLjDLMNae', 'jyzl7fgRUM', '9Qw9QivwzP', 'yusRdVhtWs', '51PVWaYGGA', '6WfXlim5Ir', '8YtcKmRzrN', '5RlYvAqTQu', 'xpMiPibFkc', 'mHpyELjw7p', 'qyB2OPwGbj', '3f55O4040h', 'lIxV1ivR5Y', 'ZZ4xd3zi1y', 'bIQDRhWwYW', 'G3MWMsi7Un', 'aHZQFAcMSK', 'ckNIIHsxHj', 'u6UfTcKRjQ', 'mTvjbb0Aax', '3VMegdS8g5', 'H1C1aPpuBs', 'mc2NKPSvst', 'OuPKIEcE2x', 'rE0YE5511Q', '7EVkUmVOfU', 'HHoULtiZQo', 'PPrAtupCE5', 'T5GZpfp6Qm', 'si0DS3Qj2L', 'O46JUqFAPB', 'nQaATZXW8D', 'oka3Y6Gdum', 'UGrQLDrkWB', 'ykpuSlbIdh', 'yQnt47o0I9', 'kPKkKYD7ix', 'FQJJjOgk6p', 'z08x0dyG4I', 'gyW3pRIVoA', 'jShPBNkY0B', 'Os68Xqou3X', 'SwmuieUI9A', '73TDBiIHAF', 'gH5Yl2Vq6H', 'yKxmbjaSUG', 'LgKPcHLW3P', 'Mwh04wRFNc', 'uyG60UJJK7', 'PU4UwGPGF3', 'eFj7zg6lmV', 'qiamfQG8Kj', 'bW0CoYdwr9', 'R5uBEU6IVv', 'l5khArgAIP', 'y9WqY8emTX', 'YIrDzys1PG', '3tK26vDvMv', 'IERYD3jdVd', '7dxKnm1sTN', 'C304u640Wh', 'acHJ43HyOz', 'JEf6BTSpet', 'gUQfyUAej7', 'uJpoWhyn9I', 'hwaGSax6ni', 'XBRUbhBDZz', 'q7KX0YSzfU', 'u0WhbRszLp', 'Bh94aeig4l', '6C3F7U7WQb', 'Bb5C9Kq8sP', 'IM0tc18Sdj', '6OJvyWsbV8', 'Ou7wYGK3af', 'UHzjGgn6PF', 'df2mmjShOI', 'qCvWYmKrRo', 'U0VzKRvBXg', 'VoeJnkiZFa', 'Yq1ODiy6p3', 'nu6pXmINBS', 'xe8s6l6P7W', 'p7xIBVME51', '899VgbYW4K', '4RYT5ttht4', 'hR28JzbWyO', '5g7DQhXctI', 'XEU2tAB9Hk', 'K7z0XYKMmW', '4ajuzON9bL', 'zSRMYJtVMX', 'Ex8ecHGQ0i', '7ObuI1Fjs8', '5dRf0wpZq0', 'p24JAm8ZFJ', 'E2NgJUHxQP', 'FaCpADOWAi', 'rkLOpy47uY', 'X2N7UNYz9u', 'KO0fz2WHI6', 'epKLFjDCUk', 'MmIPDWyH0Y', '1HiYddEbLs', 'YhCWirQN1q', 'lgdMYR9QHX', '0xdqBbWANa', 'aEvtcufbmZ', 'uXpjJNgjOs', 'XWJzx4X7m1', 'ptV6ES72O3', 'c2lYXNLAdY', '4uoDBKbNKI', 'pTjNR9AcWQ', 'gpOoA5z5Fm', 'TWVjdcXydp', 'fSfwtGH9X5', 'KeaIz2f7AI', '8Uq2BdnpGA', 'ABq2kWvvey', '1eH2cp9G8i', 'bk65RwujKI', '7va9RGd6Uk', 'MjyEw5qd22', 'BT8OJxEyWv', 'qeEB3p1F1y', 'bnpd2WypKy', '75GY0scPwI', 'dgmJpaIApi', '8Qnds3RsB6', 'UXEm00P9LI', 'wDqW2o6AVq', 'v58Yh9ngMm', 'KvPT4JATpC', 'Ub41hS6uZn', 'w7Gdd5GZBY', 'HHX8IVZgEp', 'nCA87EgRCu', 'vReiobPTNe', 'm8Z8z2OeWe', 'Zf19vweCsa', 'EWQFR1xVH8', 'emkOAUgBa1', 'o85VCfyIf6', 'c6fFsvKtpi', 'xaQ30TpjYu', 'scarrqvN8I', 'ARfmrJKj8i', 'fciHvwj5Fx', 'AnUAWjqvbE', 'VyHIDprQGz', 'F7hHcrZcuW', 'x4FmmTqfUH', 'UIQedFmBPL', 'TppERQiLRa', 'vTRsjNU0Xh', 'LrENIIiGOK', 'grpVldpvLB', 'uYAYnIC1Ng', 'eytkQjU3pI', 'W0nLyeHuMf', 'aSJuYX2mdr', 'qRLp03g8xu', 'zMIWY1SiBM', 'O8RiLuYrqW', 'YKKSxaBXb8', 'Tsw8xiskjz', 'LIkHJZZjAs', 'iwFY8uMofW', 'T3gip0c6l7', 'Yaxx87YgDJ', 'Nlcb42SsSz', 'XLVRkzJpiw', 'qxAW1UwYRG', 'wyUQq5lCkh', 'CVDXoAsFLX', 'waXXGyaCFC', 'zgkgudF9IP', 'rtIC8xuokf', 'aCCN2tYPE4', '7hTTyYgaa9', 'dCL0neFQr4', 'AXtrCJZJAR', 'xHq2ogWn8s', '9ocvpPeXuE', '2XuggVJbij', 'ZioBz9Igzm', 'NlFs0mVJEI', 'A10b3XbBBd', 'WkGIJ0XIyL', 'HvFUbp9zJy', 'jNWTbNH4KI', 'NzdofV18g7', 'WEXmOjffgB', '6DoeUiCDGz', 'ngDUWkR4Zh', 'F3Iq2STXVT', '2Mq9JdepbY', 'PNfekUDy5p', 'c3SMgY2Skh', 'PC6ZygSNEs', 'pNpxf6ZXKY', '1TkZdCLp7g', 'rtadpz2438', 'xLFvclqEjN', 'kgvtGW2v3c', 'xCa1CJ02im', 'xlavnUkThq', 'TAsSBF81u6', 'EJKpj1tBr7', 'kgOJ4dWzYG', '243erqsh1X', 'E5SeUJMaf8', 'gRwnsDyzj3', 'SvGRbgRojk', 'FASeljJg8q', 'OTOpBgUPeW', 'Rez1ytbmLE', 'BgbE3wKDV7', 'eyUEBlXnhu', '4rqu1Kxilq', '6eDNaR8UoW', 'lSko2dAPd9', 'PaZGZhW03Z', 'TSojqd2e7E', 'qWaBG6jBXx', '2DVMcggrdV', 'e6I6HAZGcY', 'WBpE9VHrZM', 'QST4CeGCe3', 'DPcoCUaYs5', 'kMhosFNn8X', 'HMHwgVyy9N', '6FRE0jjUQS', 'oBNHhib6SU', 'bfWRLrq6ML', 'TVbxg0gN7s', 'SI90N2d5LX', '3kC5iroi59', 'NHTkfPAp4p', 'ZDALB5Oy2S', 'Y3SSInv4lP', 'FbnGrw4jrC', 'kQzAa9FvDo', 'WPUjzfD5TT', 'ydvk4H6g5G', 'AmAXarY0AL', '3wTFWP9BB0', 'JzIft6nZ6x', 'DD5SXaDWHc', '5wn9zcf3Gv', '8yqb2RYnt6', 'HrMNnbMLvS', 'KKmn1jApji', '6CU4l1LXYS', 'P2iPsVd1Kz', 'eKlA2LhvDp', 'VohuQfzd6L', 'ZIxtRXI1CA', 'dkuhAZ4yWA', 'OOK9wJzTa2', 'dPzOPnm1v6', 'NozkfFim5B', 'n6LTFJuAOM', '4QUO9Ql9z8', 'LR1GMLDb0s', 'URl5zx6b0A', 'QNPudpeV5Z', 'O8A667vrRq', 'a5EtGUu6qd', 'wcyPmLAeCB', 'rxgng4kPmk', 'DLVFtOrjVn', 'TSRmpNcZl1', 'DICOI5nl7z', 'WttU65pitl', 'Cd7VrlEkez', '9a56UZV0Qd', 'nl4u4zqTLk', 'o4LdcOnriP', 'U7jiXwyXeE', 'libBJjUPAI', 'GA5XFQLllh', 'DFoA8bpNoz', 'eVNKyCzEHo', 'PVCcTPPc7q', 'OlPcIlPLe4', 'NZLLzkveOt', 'hbCZicPNtt', 'x0FxGPfPbr', 'LPQdIGSHV0', 'DLIwmsueVx', 'wKehA72sGR', 'q2odyI6bGJ', '0PokU9f49J', '4JvagmI5zc', 'Y055cRoxqD', 'WGd1Z32cqf', 'i7cecYmKI0', 'XELoaNxtQG', 'wJw4ivuij2', 'm2Y4QHmsOi', 'zs74MbRYjp', 'Q4ei34oGru', 'TvTmMge6UU', '4Azw36oExC', 'cyHDqvfQFY', 'ZKUUJHuaO2', 'b2pDlN1Cwa', '3PYkbAlKjQ', 'bxmqozPDXS', 'johzcQOfMk', 'I9cxJFQFc2', 'fEGb6xNyfc', 'CDnzDBaCD8', 'IRkJBDvcVq', 'nFsKUVpKNB', '46Ds7ncCrv', 'EJEcBTnEIw', 's01p7vanzD', 'mLSWGB1ecE', '66pC6NtD35', 'tx4PPVT5d9', 'uZl2YvIYCf', '6WiVy4qsNy', 'aIcy7Diexs', 'Zf49KmxRC5', 'Qh8gBJTIle', 'GbVh20ytRa', 'DrmxTw4Sl4', 'kAuQ70gZ7w', 'M34hq29Tdp', 'OL7d2q86mI', 'AY6V8vFOGm', 'VU3PYQBcPg', 'GqylRQ9LSy', 'aCUnD0Zy2y', 'ma8FKNxlVL', '9tgNTZVaEE', 'KQl3WXa4iu', 'GQ3mwiry8B', 'STPzrDZvFi', 'aLykccem1A', 'eYd6SVgbu4', 'QhkxEjqmT5', '1MTukmIgyS', '8VzO2BEvO2', 'gApKXqByNf', 'MzelgHeizw', 'FpuaTTHoIe', 'u3rT2sawNP', 'c67MumtfTT', 'X6e3YbYlsl', 'gzoTrr4iFq', 'TpaAWYIqXL', 'gO4Us72S75', 'RSo6GnVPUs', 'rZf9fWIlLn', 'ddoeIvzOsD', '2rVJC3ZtK4', 'WOr8QPpkFk', 'SMiuwXs2D1', 'FEUYzThSwa', 'G4ky2JqOKd', 'vny3tErGBb', 'vnPSGvXtp5', 'jLCPdR0MDq', 'TMHjIMNOet', 'toHcLthBi4', 'kDIIFxUkhs', '3ChlXO0mnO', 'gawIqkKn5N', 'SigmjlYZht', 'oTWJvdxGVd', 'GFBj8PqQME', '6pbuJ6K8WL', 'ODKiaefw5J', 'Jbu5cl8GOb', 'f1DojjkTmS', '1N9mBnowCF', 'eIUbepoNpr', 'zGojKAkozO', 'C0QbKwFRak', 'Pph678HvP9', '8SigQgTb7q', 'qaBoi9HZzo', 'ft7r1qLvaX', 'UxyCptV0B7', 'pSJqa4aTt5', '9rjGkU1GR9', '12NCw8rJpF', 'AP203BUu1J', 'XwPg8f5LK6', '1Ayjg21cQR', '36FajyZ8E6', 'sVgEfaKAqb', 'ligdVEjJMm', 'GXL7uDzxUI', 'VhCZJclGgh', 'uhJ5AXeS8P', 'x1kRUqYGCc', 'bgOHRbFVqZ', 'GizSUClrDT', 'rx7pyKSjwQ', 'vq42WMXJEO', 'kwkSQfO4Qd', 'mPcBWwqham', 'iF7p8uCMcw', 'knDQtTzoW1', 'amZVrsWAvF', 'duHM1X3JhI', 'IZraNN92t1', 'isSBEB1UnU', 'zzZ0mF5Ww6', 'bqKDfJhJTq', 'iwVm8KJSbc', 'Ab6lIJgC3l', 'A3dBX7miri', 'njeFcSC6Qw', 'SCFijhz92c', '3KSJfmEaip', 'ZN0owV1fJh', 'fX5znd2eiW', 'ibzYz0aE8Z', 'rKbmUfktWd', 'vFCEDnnOaK', 'XkhisyR23v', 'N2eYnFsvYT', 'nETiYDqThv', 'V2rd7xm08i', 'eyUOcNgEty', 'lhewffkO2c', 'fJHTozIYkU', 'l9VBAkpIp9', 'bNMJuOSZM3', 'q1Hs5fJIhC', '4akDKVtI2h', 'OVAWjrCfWQ', 'S9PxD9MB3l', 'B4w8wcTDeA', 'quFzjEJqHE', '2thkVbcMfn', 'M0I5E1KqVR', 'sZBD1IMGDX', 'KGbcnDvv8S', 'wYC3yROJIA', 'yXCUi2hURk', 'UeTQ3dA9lh', '5PsYN1Z9VU', 'KFGPM76f3E', 'esgn2kVF8H', 'iJn9RLAC5g', 'NIrhTckJIw', 'vUXT45Pc2n', 'nbzO2zhSjj', 'FRV8wFa6Yn', 'oo2VtErhRs', 'XacsSfKuU4', '3HURfXjy2i', 'pHTjSpD8Wh', 'kJpBanP3pK', 'jOhWkPNBaY', 'W71urE3aEl', 'jr4LcKnYJp', 'm9FSrOfoXd', 'Nawn0d4Ntx', 'ILUt8Dg2US', '4JhrxRpp5k', '4uo728PttK', 'qGmUl4Ui0S', '2NA7FW0zS0', 'a3OH3tcO8Z', 'RTHLzKRAOX', 'XjBkOSChP0', 'HLEn5nLRZ1', 'j9Jr1Ofi0R', 'IJERCgAfbX', 'BvNDFg0jEc', 'i5QC82bbyg', 'FzmO8bxqBM', 'Vp1gDHrdf5', 'LQMBtxuuXs']
# 创建Redis连接
client = redis.Redis(host='localhost', port=6379, db=0)

# 定义随机生成键和值的函数
def random_key_value():
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    value = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return key, value

# 执行100个随机操作
for _ in range(100):
    # 随机选择是进行读操作还是写操作
    operation = random.choice(['read', 'write'])
    
    # 执行写操作
    if operation == 'write':
        key, value = random_key_value()
        client.set(key, value)
        print(f"Set: {key} => {value}")
    
    # 执行读操作
    else:
        # 为了确保有键可以读取，我们先创建一个键
        key = random.choice(keysList)
        value = client.get(key)
        print(f"Get: {key} => {value}")