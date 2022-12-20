// Copyright 2019 The TensorFlow Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ==============================================================================

export async function render() {
    const msg = createElement('p', 'Fetching data…');
    document.body.appendChild(msg);

    const runToTags = await fetch('./tags').then((response) => response.json());
    const data = await Promise.all(
        Object.entries(runToTags).flatMap(([run, tagToDescription]) =>
            Object.keys(tagToDescription).map((tag) =>
                fetch('./greetings?' + new URLSearchParams({run, tag}))
                    .then((response) => response.json())
                    .then(response => {
                        console.log(response);
                        return response
                    })
                    .then((greetings) => ({
                        run,
                        tag,
                        greetings,
                    }))
            )
        )
    );

    const style = createElement(
        'style',
        `
      thead {
        border-bottom: 1px black solid;
        border-top: 2px black solid;
      }
      tbody {
        border-bottom: 2px black solid;
      }
      table {
        border-collapse: collapse;
      }
      td,
      th {
        padding: 2pt 8pt;
        text-align: left;
      }
    `
    );
    style.innerText = style.textContent;
    document.head.appendChild(style);

    const table = createElement('table', [
        createElement(
            'thead',
            createElement('tr', [
                createElement('th', 'Run'),
                createElement('th', 'Tag'),
                createElement('th', 'Repository'),
                createElement('th', 'Branch'),
                createElement('th', 'Last Commit'),
                createElement('th', 'Last Upstream Commit'),
                createElement('th', 'Patch'),
                createElement('th', 'Upstream Patch'),
            ])
        ),
        createElement(
            'tbody',
            data.flatMap(({run, tag, greetings}) =>
                greetings.map((guest, i) => {
                        const rowData = JSON.parse(guest)
                        return createElement('tr', [
                            createElement('td', i === 0 ? run : null),
                            createElement('td', i === 0 ? tag : null),
                            createElement('td', renderRepo(rowData.remote_url)),
                            createElement('td', rowData.branch),
                            createElement('td', renderCommit(rowData.last_commit)),
                            createElement('td', renderCommit(rowData.last_upstream)),
                            createElement('td', renderPatch(rowData.patch, 'diff.patch')),
                            createElement('td', renderPatch(rowData.upstream_patch, 'upstream.patch')),

                            // createElement('td', description),
                        ]);
                    }
                )
            )
        ),
    ]);
    msg.textContent = 'Data loaded.';
    document.body.appendChild(table);
}

function createElement(tag, children) {
    const result = document.createElement(tag);
    if (children != null) {
        if (typeof children === 'string') {
            result.textContent = children;
        } else if (Array.isArray(children)) {
            for (const child of children) {
                result.appendChild(child);
            }
        } else {
            result.appendChild(children);
        }
    }
    return result;
}

function renderRepo(repoString) {
    const [gituserDomain, userRepo] = repoString.split(':');
    const [gituser, domain] = gituserDomain.split('@');
    const [user, ...repo] = userRepo.split('/');
    const [repoName, _] = repo.join().split('.');
    const href = `${domain}/${user}/${repoName}`;
    const link = document.createElement('a');
    link.href = 'https://' + href;
    link.textContent = repoName;
    link.target = '_blank';
    console.log({
        gituserDomain, user, repo, href
    });
    return link;
}
function renderCommit(commit) {
    const element = document.createElement('a');
    element.textContent = commit;
    element.title = 'Click to copy';
    element.onclick = () => copyToClipboard(commit);
    element.style.cursor = 'pointer';
    element.style.color = 'blue';
    element.style.textDecoration = 'underline';
    return element;
}

function renderPatch(patch, downloadName) {
    const link = document.createElement('a')
    link.textContent = 'Download'
    link.onclick = function () {
        download(downloadName, patch)
    }
    link.style.cursor = 'pointer';
    link.style.color = 'blue';
    link.style.textDecoration = 'underline';
    // link.target = '_blank'
    return patch ? link : 'No Changes';
}

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text);
}