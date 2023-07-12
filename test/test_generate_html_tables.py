import pandas as pd
from src.generate_html_tables import generate_html_tables


class TestGenerateHTMLTables():

    def test_generate_single_table(self):
        input_df = pd.DataFrame({
            "service_name": ["test service name"],
            "organisation": ["test organisation"],
            "description": ["test description"],
            "attending_type": ["test attending type"],
            "website": ["test-website.com"],
            "telephone": ["test telephone"],
            "email": ["test-email@test.com"],
            "last_assured_date": ["12/07/2023"],
        })
        service_name = "test service name"
        organisation = "test organisation"
        description = "test description"
        attending_type = "test attending type"
        website = "test-website.com"
        telephone = "test telephone"
        email = "test-email@test.com"
        last_assured_date = "12/07/2023"
        expected_out = [f"""<table>
    <thead>
        <tr>
            <th>Service Name&ensp;</th>
            <td class="serviceName">
                {service_name}
            </td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan="2">
                <p class="organisation">
                    <b>Organisation:&ensp;</b>
                    {organisation}
                </p>
                <b>Description:</b>
                <p class="description">
                    {description}
                </p>
                <b>Attending Type: </b>
                <p class="attendingType">
                    {attending_type}
                </p>
            </td>
        </tr>
        <tr>
            <td colspan="2">
                    <b>Website:</b>
                    <p class="oneLineInfo">
                    {website}
                    </p class="oneLineInfo">
                    <b>Telephone: </b>
                    <p>
                        {telephone}
                    </p>
                    <b>Email: </b>
                    <p class="oneLineInfo">
                        {email}
                    </p>
            </td>
        </tr>
        <tr>
            <td colspan="2">
                <p><b>Last Assured:&ensp;</b>{last_assured_date}</p>
            </td>
        </tr>
    </tbody>
</table>"""]
        assert expected_out == generate_html_tables(input_df)
