import pytest
from Wingman.core.status_indicator import StatusIndicator
class TestStatusIndicator:
    @pytest.mark.parametrize("statusIndicator,stringRepresentation", argvalues=[
                                                                    (StatusIndicator.BLEED, "B"),
                                                                    (StatusIndicator.POISON, "P"),
                                                                    (StatusIndicator.DISEASE, "D"),
                                                                    (StatusIndicator.STUN, "S"),
                                                                    (StatusIndicator.BLEED | StatusIndicator.POISON, "BP"),
                                                                    (StatusIndicator.BLEED | StatusIndicator.DISEASE, "BD"),
                                                                    (StatusIndicator.BLEED | StatusIndicator.STUN, "BS"),
                                                                    (StatusIndicator.POISON | StatusIndicator.DISEASE, "PD"),
                                                                    (StatusIndicator.POISON | StatusIndicator.STUN, "PS"),
                                                                    (StatusIndicator.DISEASE | StatusIndicator.STUN, "DS"),
                                                                    (StatusIndicator.BLEED | StatusIndicator.POISON | StatusIndicator.DISEASE, "BPD"),
                                                                    (StatusIndicator.BLEED | StatusIndicator.POISON | StatusIndicator.STUN, "BPS"),
                                                                    (StatusIndicator.BLEED | StatusIndicator.DISEASE | StatusIndicator.STUN, "BDS"),
                                                                    (StatusIndicator.POISON | StatusIndicator.DISEASE | StatusIndicator.STUN, "PDS"),
                                                                    (StatusIndicator.BLEED | StatusIndicator.POISON | StatusIndicator.DISEASE | StatusIndicator.STUN, "BPDS")
                                                                    ]
    )
    def test_CompareStatusIndicators_AgainstTheirStringRepresentation(self, statusIndicator, stringRepresentation):
        assert statusIndicator == stringRepresentation
    
    def test_Against_None_NotEqualPasses(self):
        statusIndicator = StatusIndicator.BLEED
        assert statusIndicator != None
    
    def test_Against_None_EqualPasses(self):
        statusIndicator = StatusIndicator.BLEED
        assert not statusIndicator == None
    
    def test_NoStatusAilment(self):
        assert '' == StatusIndicator(0)
    
    @pytest.mark.parametrize("stringRepresentation,expectedStatusIndicator", argvalues=[
                                                                            ("B", StatusIndicator.BLEED),
                                                                            ("P", StatusIndicator.POISON),
                                                                            ("D", StatusIndicator.DISEASE),
                                                                            ("S", StatusIndicator.STUN),
                                                                            ("BP", StatusIndicator.BLEED | StatusIndicator.POISON),
                                                                            ("BD", StatusIndicator.BLEED | StatusIndicator.DISEASE),
                                                                            ("BS", StatusIndicator.BLEED | StatusIndicator.STUN),
                                                                            ("PD", StatusIndicator.POISON | StatusIndicator.DISEASE),
                                                                            ("PS", StatusIndicator.POISON | StatusIndicator.STUN),
                                                                            ("DS", StatusIndicator.DISEASE | StatusIndicator.STUN),
                                                                            ("BPD", StatusIndicator.BLEED | StatusIndicator.POISON | StatusIndicator.DISEASE),
                                                                            ("BPS", StatusIndicator.BLEED | StatusIndicator.POISON | StatusIndicator.STUN),
                                                                            ("BDS", StatusIndicator.BLEED | StatusIndicator.DISEASE | StatusIndicator.STUN),
                                                                            ("PDS", StatusIndicator.POISON | StatusIndicator.DISEASE | StatusIndicator.STUN),
                                                                            ("BPDS", StatusIndicator.BLEED | StatusIndicator.POISON | StatusIndicator.DISEASE | StatusIndicator.STUN)
                                                                            ]
    )
    def test_CreateStatusIndicatorFromString(self, stringRepresentation, expectedStatusIndicator: StatusIndicator):
        statusIndicator: StatusIndicator = StatusIndicator.FromString(stringRepresentation)

        assert statusIndicator == expectedStatusIndicator
