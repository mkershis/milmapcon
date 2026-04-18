import pytest
import milmapcon as mmc 

@pytest.mark.parametrize(
    'label,grid_reference,grid_letters_test,clean_grid_test,x_m_test,y_m_test',
    [
        ('valid_four_digit_grid','vS0144','vS','vS0144',1000,44000),
        ('valid_six_digit_grid','vS014448','vS','vS014448',1400,44800),
        ('invalid_grid_numbers','vS014','vS','vS014',None,None)
    ]
)
def test_parse_gridsquare(label, grid_reference, grid_letters_test,clean_grid_test, x_m_test, y_m_test):

    grid_letters, clean_grid, x_m, y_m = mmc.parse_gridsquare(grid_reference)

    assert (grid_letters, clean_grid, x_m, y_m) == (grid_letters_test, clean_grid_test, x_m_test, y_m_test), f'Test failed for {grid_reference} in {label} test'