            // create form for factor input
            let form1 = document.createElement("form");
            form1.setAttribute("method", "post");
            form1.setAttribute("action", "submit.php");
            var form1input = document.createElement("input");
            form1input.setAttribute("type", "text");
            form1input.setAttribute("name", "Factors_of_)C");
            form1input.setAttribute("placeholder", "Factors of C");
            // create a submit button
            var s = document.createElement("input");
            s.setAttribute("type", "submit");
            s.setAttribute("value", "Submit");
            // Append the full name input to the form
            form1.appendChild(form1input);
            // Append the submit button to the form
            form1.appendChild(s);